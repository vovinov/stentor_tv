from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.news.models import News
from apps.rundowns.forms import RundownsDateForm
from apps.rundowns.models import Rundown, RundownNews


@login_required
def index_get(request):
    return render(request, "index.html")


def rundowns_manage(request):

    if request.method == "POST":
        date = int(request.POST["date"].split("-")[-1])
        form = RundownsDateForm(request.POST)

        rundowns = Rundown.objects.filter(air_day=date)
        print(rundowns)
        return render(
            request,
            "rundowns/rundown_manage.html",
            {"form": form, "rundowns": rundowns},
        )

    else:
        form = RundownsDateForm()
        return render(request, "rundowns/rundown_manage.html", {"form": form})


def rundowns_detail(request, rundown_id):
    rundown = Rundown.objects.get(id=rundown_id)

    return render(
        request,
        "rundowns/rundown_detail.html",
        context={"rundown": rundown},
    )


def rundowns_create(request):

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
    )
    current_news = rundown.news.all()

    for n in current_news:
        RundownNews.objects.create(rundown=rundown_new, news=n)

    if not created:
        return redirect("rundowns:rundown_manage")
    else:
        return redirect("rundowns:rundown_detail", rundown_id=rundown_new.id)
