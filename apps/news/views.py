from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.db.models import Q

from apps.rundowns.models import Rundown, RundownNews

from .models import News
from .forms import NewsCreationForm, NewsEditForm


def manage_news(request):
    news = News.objects.all()

    context = {"news": news, "form": NewsCreationForm()}

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
        news.user = request.user
        news.save()

        rundown = Rundown.objects.all().first()

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

    return render(request, "news/components/news_item.html", context)


class NewsUpdateView(UpdateView):

    model = News
    form_class = NewsEditForm
    template_name = "news/news_edit.html"
    success_url = reverse_lazy("news:news_content")


def news_delete(request, item_id):
    rundown_news = RundownNews.objects.get(id=item_id)
    rundown_news.delete()
    return redirect("rundowns:rundown_get", rundown_id=rundown_news.rundown.id)
