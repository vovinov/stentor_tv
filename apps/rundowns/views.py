from datetime import datetime
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.rundowns.models import Rundown


def rundown_get_last(request):
    rundown = Rundown.objects.all().first()
    rundown_news = Rundown.objects.all().first().rundowns_items.order_by("position")

    return render(
        request,
        "rundowns/rundown.html",
        context={"rundown_news": rundown_news, "rundown": rundown},
    )


@require_POST
def rundown_create(request):
    air_date = request.POST.get("air_time")
    air_time = request.POST.get("air_date")
    if air_date:
        dt = datetime.fromisoformat(air_date)  # дата без времени
        dt = datetime.combine(dt.date(), time(11, 0))
        dt = timezone.make_aware(dt)
    else:
        dt = timezone.now()

    Rundown.objects.create(title="123", air_datetime=dt)
    return redirect("index")
