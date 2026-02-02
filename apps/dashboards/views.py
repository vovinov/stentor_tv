from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from apps.news.models import News
from apps.rundowns.models import Rundown


@login_required
def view_dashboard(request):

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
    news = News.objects.filter(editor=request.user)
    context = {"news": news}

    return render(request, "news/news_manage.html", context)


@login_required
def view_for_mont(request):
    news = News.objects.all().order_by("-updated_at")

    context = {"news": news}

    return render(request, "news/news_manage.html", context)


@login_required
def view_for_release(request):
    news = News.objects.all().order_by("-updated_at")

    context = {"news": news}

    return render(request, "news/news_manage.html", context)
