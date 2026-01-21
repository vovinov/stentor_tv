from django.utils import timezone
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.rundowns.models import Rundown
from utils import round_to_hour


def index_get(request):
    return render(request, "index.html")


def rundowns_manage(request):
    today = timezone.localtime()
    rundowns = Rundown.objects.filter(air_date__day=today.day)

    return render(
        request,
        "rundowns/rundown_manage.html",
        context={"today": today, "rundowns": rundowns},
    )


def rundown_get(request, rundown_id):
    rundown = Rundown.objects.get(id=rundown_id)

    return render(
        request,
        "rundowns/rundown.html",
        context={"rundown": rundown},
    )


def rundowns_create(request):
    rundown, created = Rundown.objects.get_or_create(
        air_date=round_to_hour(timezone.localtime())
    )

    if not created:
        redirect("index")
    else:
        return redirect("rundowns:rundown_get", rundown_id=rundown.id)


# rundown_news = Rundown.objects.all().first().rundowns_items.order_by("position")
