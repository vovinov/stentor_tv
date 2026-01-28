from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.contrib import messages

from apps.assets.models import Asset
from apps.rundowns.models import Rundown, RundownNews
from apps.statuses.models import Status

from .models import News
from .forms import NewsCreationForm, NewsEditForm


def manage_news(request):
    news = News.objects.all()

    context = {"news": news, "form": NewsCreationForm(), "add": False}

    return render(request, "news/news_manage.html", context)


def search_news(request):
    search = request.GET.get("search", "")
    news = News.objects.filter(Q(title__icontains=search))

    context = {"news": news, "form": NewsCreationForm()}

    return render(request, "news/components/news_list.html", context)


def create_news(request):
    form = NewsCreationForm(request.POST)

    if form.is_valid():
        news = form.save(commit=False)

        news.created_by = request.user
        news.updated_by = request.user

        status = Status.objects.get(id=1)
        news.status = status
        news.save()

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

    RundownNews.objects.get_or_create(
        rundown=rundown, news=news, position=len(rundown.news.all()) + 1
    )

    messages.success(request, "Новость успешно добавлена!")

    return redirect("rundowns:get_rundown_detail", rundown.id)


class NewsUpdateView(UpdateView):

    model = News
    fields = ["title", "content"]
    template_name = "news/news_edit.html"
    success_url = reverse_lazy("news:manage_news")


def delete_news_from_rundown(request, item_id):
    rundown_news = RundownNews.objects.get(id=item_id)
    rundown_news.delete()

    messages.success(request, "Новость успешно удалена из выпуска!")

    return redirect("rundowns:get_rundown_detail", rundown_id=rundown_news.rundown.id)


def view_assets_to_add_news(request, news_id):
    news = News.objects.get(id=news_id)
    assets = Asset.objects.exclude(id=news.asset.id)

    context = {"assets": assets, "news_id": news_id}

    return render(request, "assets/assets_change.html", context)


def change_asset_news(request, news_id, asset_id):
    news = News.objects.get(id=news_id)
    asset = Asset.objects.get(id=asset_id)

    news.asset = asset
    news.save()

    messages.success(request, "Материал успешно изменён")

    return render(request, "index.html")
