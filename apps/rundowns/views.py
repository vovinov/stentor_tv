from django.utils import timezone
from datetime import time, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth import get_user_model

from apps.rundowns.forms import RundownsDateForm
from apps.rundowns.models import Rundown, RundownNews
from utils import add_time


@login_required
def get_index(request):
    return render(request, "index.html")


def manage_rundowns(request):

    html = "rundowns/rundown_manage.html"

    if request.method == "POST":
        date = int(request.POST["date"].split("-")[-1])

        rundowns = Rundown.objects.filter(air_day=date)
        return render(
            request,
            html,
            {"rundowns": rundowns},
        )

    else:
        form = RundownsDateForm()
        return render(request, html, {"form": form})


def get_rundown_detail(request, rundown_id):
    rundown = Rundown.objects.get(id=rundown_id)

    start_hour = time(rundown.air_hour, 0, 0)
    temp = "A"

    for pos, r in enumerate(rundown.rundown.all(), 1):

        if pos == 1:
            r.start_time = start_hour
        else:
            r.start_time = temp

        if r.news.asset:
            r.end_time = add_time(r.start_time, r.news.asset.duration)
        else:
            r.end_time = r.start_time

        temp = r.end_time

        r.save()

    context = {"rundown": rundown}

    return render(
        request,
        "rundowns/rundown_detail.html",
        context,
    )


def create_rundown(request):

    current_hour = timezone.localtime().hour

    next_hour = 0 if current_hour == 23 else current_hour + 1

    if next_hour != 0:
        current_day = timezone.localtime().day
    else:
        current_day = timezone.localtime().day + 1

    current_year = timezone.localtime().year
    current_month = timezone.localtime().month

    rundown = Rundown.objects.all().first()

    rundown_new, created = Rundown.objects.get_or_create(
        air_year=current_year,
        air_month=current_month,
        air_day=current_day,
        air_hour=next_hour,
        created_by=request.user,
        updated_by=request.user,
    )

    current_news = rundown.news.all()

    for pos, n in enumerate(current_news, 1):
        RundownNews.objects.create(rundown=rundown_new, news=n, position=pos)

    return redirect("rundowns:manage_rundowns")


def get_rundowns_by_date(request):
    day = request.POST.get("date", "").split("-")[-1]
    rundowns = Rundown.objects.filter(air_day=int(day))

    context = {"rundowns": rundowns}

    return render(request, "rundowns/components/rundown_list.html", context)


def change_news_position_down(request, rundown_news_id):
    rundown_news = RundownNews.objects.get(id=rundown_news_id)

    after_pos = RundownNews.objects.get(
        Q(rundown=rundown_news.rundown.pk) & Q(position=rundown_news.position + 1)
    )

    after_pos.position = rundown_news.position
    rundown_news.position += 1

    after_pos.save()
    rundown_news.save()

    rundown = Rundown.objects.get(id=rundown_news.rundown.pk)
    context = {"rundown": rundown}

    return render(request, "rundowns/components/rundown_ul.html", context)


def change_news_position_up(request, rundown_news_id):
    rundown_news = RundownNews.objects.get(id=rundown_news_id)

    before_pos = RundownNews.objects.get(
        Q(rundown=rundown_news.rundown.pk) & Q(position=rundown_news.position - 1)
    )

    before_pos.position = rundown_news.position
    rundown_news.position -= 1

    before_pos.save()
    rundown_news.save()

    rundown = Rundown.objects.get(id=rundown_news.rundown.pk)
    context = {"rundown": rundown}

    return render(request, "rundowns/components/rundown_ul.html", context)
