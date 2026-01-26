from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.news.models import News
from apps.rundowns.forms import RundownsDateForm
from apps.rundowns.models import Rundown, RundownNews


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

    p = 0
    for pos, r in enumerate(rundown.rundown.all(), 1):
        r.position = pos
        r.save()

    context = {"rundown": rundown}

    return render(
        request,
        "rundowns/rundown_detail.html",
        context,
    )


def create_rundown(request):

    current_year = timezone.localtime().year
    current_month = timezone.localtime().month
    current_day = timezone.localtime().day
    current_hour = timezone.localtime().hour

    rundown = Rundown.objects.all().first()

    rundown_new, created = Rundown.objects.get_or_create(
        air_year=current_year,
        air_month=current_month,
        air_day=current_day,
        air_hour=current_hour + 1,
        creator=request.user,
    )

    current_news = rundown.news.all()

    for n in current_news:
        RundownNews.objects.create(rundown=rundown_new, news=n)

    context = {"rundown_id": rundown_new.id}

    if not created:
        return redirect("rundowns:manage_rundown")
    else:
        return render(request, "rundowns/rundown_detail.html", context)


def get_rundowns_by_date(request):
    day = request.POST.get("date", "").split("-")[-1]
    rundowns = Rundown.objects.filter(air_day=int(day))

    context = {"rundowns": rundowns}

    return render(request, "rundowns/components/rundown_list.html", context)
