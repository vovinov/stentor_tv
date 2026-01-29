from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from apps.rundowns.models import Rundown


@login_required
def view_dashboard(request):

    user = request.user
    print(user.groups.filter(name="boss").exists())

    if user.groups.filter(name="boss").exists():
        return redirect("dashboards:view_for_boss")

    if user.groups.filter(name="editor").exists():
        return redirect("dashboards:view_for_editor")


def view_for_boss(request):
    today = timezone.now()
    rundowns = Rundown.objects.filter(air_day=today.day)[:5]

    context = {"rundowns": rundowns}
    return render(request, "index.html", context)


def view_for_editor(request):
    return render(request, "news/news_manage.html")
