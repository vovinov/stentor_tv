from django import forms
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from apps.assets.models import Asset
from apps.comments.models import Comment
from apps.rundowns.models import Rundown, RundownNews
from apps.statuses.models import Status

from .models import News
from .forms import (
    NewsAddCommentForm,
    NewsCreationForm,
    NewsEditForm,
)

from simple_history.utils import update_change_reason


def view_news_history(request, news_id):
    news = News.objects.get(id=news_id)

    context = {"news": news}

    return render(request, "news/news_history.html", context)


def manage_news(request):

    group_boss = request.user.groups.filter(name="boss").exists()

    if group_boss:
        news = News.objects.all().order_by("-updated_at")
    else:
        news = News.objects.filter(editor=request.user).order_by("-updated_at")

    context = {"news": news, "form": NewsCreationForm(), "add": False}

    return render(request, "news/news_manage.html", context)


def search_news(request):
    search = request.GET.get("search", "")
    news = News.objects.filter(title__icontains=search).order_by("-created_at")

    context = {"news": news, "form": NewsCreationForm}

    return render(request, "news/components/news_list.html", context)


def create_news(request):
    form = NewsCreationForm(request.POST)

    if form.is_valid():
        news = form.save(commit=False)

        status = Status.objects.get(id=1)
        news.status = status
        news.save(user=request.user)

        try:
            rundown = Rundown.objects.all().first()
        except:
            messages.error(request, "Ошибка! Нет ни одного плейлиста!")

        last_pos = (
            RundownNews.objects.filter(rundown=rundown)
            .order_by("-position")
            .values_list("position", flat=True)
            .first()
            or 0
        )

        RundownNews.objects.get_or_create(
            rundown=rundown, news=news, defaults={"position": last_pos + 1}
        )

        context = {"n": news}

        response = render(request, "news/components/news_item.html", context)
        response["HX-Trigger"] = "success"

        messages.success(request, "Новость успешно создана!")

        return response


def show_news_to_add_rundown(request, rundown_id):
    rundown = Rundown.objects.get(id=rundown_id)
    news = News.objects.exclude(rundown_news__in=rundown.rundown_news.all()).order_by(
        "-created_at"
    )

    context = {"news": news, "rundown": rundown, "add": True}

    return render(request, "news/news_manage.html", context)


def add_news_to_rundown(request, rundown_id, news_id):
    rundown = Rundown.objects.get(id=rundown_id)
    news = News.objects.get(id=news_id)

    RundownNews.objects.create(
        rundown=rundown, news=news, position=len(rundown.news.all()) + 1
    )

    if news.asset:
        rundown.duration += news.asset.duration

    rundown.save()
    update_change_reason(rundown, f"Добавлена новость - {news}")
    messages.success(request, "Новость успешно добавлена!")

    return redirect("rundowns:get_rundown_detail", rundown.id)


class NewsUpdateView(UpdateView):
    
    model = News
    form_class = NewsEditForm
    template_name = "news/news_edit.html"

    def get_context_data(self, **kwargs):

        news = self.object

        now = timezone.now()

        is_locked_for_me = (
            news.locked_until and 
            news.locked_until > now and 
            news.locked_by != self.request.user
        )

        if not is_locked_for_me:
            # Захватываем lock
            News.objects.filter(id=news.id).update(
                locked_by=self.request.user,
                locked_until=now + timezone.timedelta(minutes=1)
            )
        
        context = super().get_context_data(**kwargs)

        context.update({
            'is_locked': is_locked_for_me,
            'lock_info': {
                'username': news.locked_by.username if news.locked_by else None,
                'until': news.locked_until
            } if is_locked_for_me else None,
            'my_lock_id': news.id
        })

        return context

    def get_form(self):
        form = super().get_form()

        if self.request.user.groups.filter(name='editor').exists():

            form.fields['status'].queryset = Status.objects.filter(title="Монтаж")
            form.fields['comment'].widget = forms.HiddenInput()
            form.fields['comment'].label = ""
            form.fields['comment'].required = False
        
        return form

    def form_valid(self, form):
        form.instance.updated_by = self.request.user

        if form.cleaned_data["comment"]:

            news = self.object

            comment, created = Comment.objects.get_or_create(
            text=form.cleaned_data["comment"],
            news=news,
            author=self.request.user,
            updated_by=self.request.user,
            )

            if created:
                news.comment.add(comment)
                news.save(user=self.request.user)
                update_change_reason(news, f"Добавлен комментарий -- {comment.text}")
                messages.success(self.request, "Комментарий добавлен!")
            else:
                messages.error(self.request, "Ошибка!")    

        return super().form_valid(form)

    def get_success_url(self):

        if self.request.user.groups.filter(name='editor').exists():
            self.success_url = reverse_lazy("dashboards:view_for_editor")
        else:
            self.success_url = reverse_lazy("news:manage_news")
        return super().get_success_url()
    
    def post(self, request, *args, **kwargs):
        news = self.get_object()

        now = timezone.now()
        
        # Проверяем lock на POST
        is_locked_for_me = (
            news.locked_until and 
            news.locked_until > now and 
            news.locked_by != request.user
        )
        
        if is_locked_for_me:
            return JsonResponse({
                'error': f'Новость редактирует {news.locked_by.username}'
            }, status=423)
        
        response = super().post(request, *args, **kwargs)
    
        News.objects.filter(id=news.id).update(
            locked_by=None,
            locked_until=None
        )

        return response

@require_http_methods(["POST"])
@csrf_exempt
def heartbeat_lock(request, pk):
    news = get_object_or_404(News, pk=pk)
    now = timezone.now()
    
    if (news.locked_by == request.user and 
        news.locked_until and 
        news.locked_until > now):
        
        News.objects.filter(id=pk).update(
            locked_until = now + timezone.timedelta(minutes=1)
        )
        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'error': 'no permission'}, status=403)


def delete_news_from_rundown(request, item_id):
    rundown_news = RundownNews.objects.get(id=item_id)
    rundown = Rundown.objects.get(id=rundown_news.rundown.id)
    news = News.objects.get(id=rundown_news.news.id)

    rundown_news.delete()
    if news.asset:
        rundown.duration -= news.asset.duration

    rundown.save()
    update_change_reason(rundown, f"Удалена из выпуска новость - {news}")
    messages.success(request, "Новость успешно удалена из выпуска!")

    return redirect("rundowns:get_rundown_detail", rundown_id=rundown_news.rundown.id)


def show_assets_to_add_news(request, news_id):
    news = News.objects.get(id=news_id)

    if request.user.groups.filter(name="mont").exists():
        assets = Asset.objects.filter(created_by=request.user)
    else:
        assets = Asset.objects.all()

    context = {"assets": assets, "news_id": news_id}

    return render(request, "assets/assets_change.html", context)


def change_asset_news(request, news_id, asset_id):
    news = News.objects.get(id=news_id)
    asset = Asset.objects.get(id=asset_id)

    news.asset = asset
    news.save(user=request.user)
    update_change_reason(news, f"Изменён материал на {asset.title}")

    messages.success(request, "Материал успешно изменён")

    return render(request, "index.html")


def change_news_status(request, news_id):

    status = request.GET["news_status"]

    news = News.objects.get(id=news_id)

    news.status = Status.objects.get(title=status)
    news.save(user=request.user)

    update_change_reason(news, f"Изменён статус на {news.status.title}")

    if status == "Правка":
        form = NewsAddCommentForm()
        context = {"news_id": news_id, "form": form}
        
        return render(
            request, "rundowns/components/rundown_change_status.html", context
        )

    context = {"n":news}
    
    return render(request, "news/components/news_item.html", context)

def add_comment_to_news(request):

    news = News.objects.get(id=int(request.POST["news_id"]))

    comment, created = Comment.objects.get_or_create(
        text=request.POST["comment"],
        news=news,
        author=request.user,
        updated_by=request.user,
    )

    if created:
        news.comment.add(comment)
        news.save(user=request.user)
        update_change_reason(news, f"Добавлен комментарий -- {comment.text}")
    else:
        messages.error(request, "Ошибка!")
        return redirect("view_dashboard")

    messages.success(request, "Комментарий добавлен!")
    return render(request, "index.html")


def delete_comment_from_news(request, news_id, comment_id):
    news = News.objects.get(id=news_id)
    comment = Comment.objects.get(id=comment_id)
    news.save(user=request.user)
    update_change_reason(news, f"Удалён комментарий -- {comment.text}")
    comment.delete()

    messages.success(request, "Комментарий удалён!")
    return redirect("dashboards:mont")
