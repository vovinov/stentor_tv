from datetime import datetime, time
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.rundowns.models import Rundown

def rundown_get_last(request):
    today = timezone.localdate()
    rundown = Rundown.objects.filter(air_date__date=today)

    if not rundown.exists():
        return HttpResponseBadRequest("rundown missing")
    
    return render(request, "rundowns/rundown.html", context={"rundown": rundown, "selected_date": today})

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

    Rundown.objects.create(title= "123",air_datetime=dt)
    return redirect("index")

def get_selected_day(request):

    selected_date = request.GET.get("date")  # YYYY-MM-DD или None
    print(selected_date)

    rundowns = Rundown.objects.filter().order_by("air_time")
    if selected_date:
        rundowns = rundowns.filter(air_datetime__date=selected_date)

    return render(request, "rundowns/rundown.html", {
        "rundowns": rundowns,
        "selected_date": selected_date,
    })

