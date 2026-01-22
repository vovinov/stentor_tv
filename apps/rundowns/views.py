from django.utils import timezone

from django.shortcuts import redirect, render


from apps.rundowns.forms import RundownsDateForm
from apps.rundowns.models import Rundown
from utils import round_to_hour


def index_get(request):
    return render(request, "index.html")


def rundowns_manage(request):

    if request.method == "POST":
        date = request.POST.get("date")
        rundowns = Rundown.objects.filter(air_date=date)
        return render(request, "rundowns/rundown_manage.html", {"rundowns": rundowns})

    else:
        form = RundownsDateForm()
        return render(request, "rundowns/rundown_manage.html", {"form": form})


def rundowns_detail(request, rundown_id):
    rundown = Rundown.objects.get(id=rundown_id)

    return render(
        request,
        "rundowns/rundowns_detail.html",
        context={"rundown": rundown},
    )

    rundown = Rundown.objects.get(id=rundown_id)

    return render(
        request,
        "rundowns/rundown.html",
        context={"rundown": rundown},
    )


def rundowns_create(request):

    today = timezone.localtime()

    current_year = str(today.day)
    current_month = str(today.month)
    current_day = str(today.day)

    air_date = f"{current_year}-{current_month}-{current_day}"
    air_time = today.hour

    rundown, created = Rundown.objects.get_or_create(
        air_date=air_date, air_time=air_time
    )

    if not created:
        redirect("index")
    else:
        return redirect("rundowns:rundown_get", rundown_id=rundown.id)


# rundown_news = Rundown.objects.all().first().rundowns_items.order_by("position")
