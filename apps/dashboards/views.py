from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from apps.assets.forms import AssetCreationForm
from apps.news.models import News
from apps.statuses.models import Status
from utils import clean_all_news_locks


@login_required
def view_dashboard(request):

    clean_all_news_locks()

    user = request.user

    if user.groups.filter(name="boss").exists():
        return redirect("dashboards:view_for_boss")

    if user.groups.filter(name="editor").exists():
        return redirect("dashboards:view_for_editor")

    if user.groups.filter(name="mont").exists():
        return redirect("dashboards:view_for_mont")

    if user.groups.filter(name="release").exists():
        return redirect("dashboards:view_for_release")


@login_required
def view_for_boss(request):

    return render(request, "index.html")


@login_required
def view_for_editor(request):

    clean_all_news_locks()
    status = Status.objects.get(title="Текст")
    news = News.objects.filter(Q(editor=request.user) & Q(status=status))
    context = {"news": news}

    return render(request, "news/news_manage.html", context)


@login_required
def view_for_mont(request):
    clean_all_news_locks()
    status = Status.objects.filter(title__in=["Монтаж", "Правка"])
    news = News.objects.filter(status__in=status).order_by("-updated_at")

    context = {"news": news, "form": AssetCreationForm()}

    return render(request, "news/news_manage.html", context)


@login_required
def view_for_release(request):
    clean_all_news_locks()
    news = News.objects.all().order_by("-updated_at")

    context = {"news": news}

    return render(request, "news/news_manage.html", context)
