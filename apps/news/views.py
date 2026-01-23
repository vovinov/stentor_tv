from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.utils import timezone

from apps.rundowns.models import Rundown, RundownNews

from .models import News
from .forms import NewsEditForm


def news_content(request):

    if request.method == "POST":
        title = request.POST["title"]
        news = News.objects.filter(title__icontains=title)

        return render(request, "news/news_content.html", {"news": news})
    else:
        news = News.objects.all().order_by("created")
        return render(request, "news/news_content.html", {"news": news})


def news_create_form(request):
    return render(request, "news/news_create.html")


def news_create(request):

    title = request.POST.get("title")
    content = request.POST.get("content")
    user = request.POST.get("user")

    news, created = News.objects.get_or_create(
        title=title, content=content, creator=user
    )

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

    return redirect("rundowns:rundown_detail", rundown_id=rundown.id)


class NewsUpdateView(UpdateView):

    model = News
    form_class = NewsEditForm
    template_name = "news/news_edit.html"
    success_url = reverse_lazy("news:news_content")


def news_delete(request, item_id):
    rundown_news = RundownNews.objects.get(id=item_id)
    rundown_news.delete()
    return redirect("rundowns:rundown_get", rundown_id=rundown_news.rundown.id)
