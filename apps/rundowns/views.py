from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages

from apps.rundowns.forms import RundownsDateForm
from apps.rundowns.models import Rundown, RundownNews

from utils import get_times


def view_rundown_history(request, rundown_id):
    rundown = Rundown.objects.get(id=rundown_id)

    context = {"rundown": rundown}

    return render(request, "rundowns/rundown_history.html", context)


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

    context = {"rundown": rundown, "rundown_items": get_times(rundown)}

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

    if not created:
        messages.error(request, "Выпуск не создан!")
        return render(request, "rundowns/rundown_manage.html")

    current_news = rundown.news.all()  # type: ignore

    for pos, n in enumerate(current_news, 1):
        RundownNews.objects.create(rundown=rundown_new, news=n, position=pos)

    messages.success(request, "Выпуск на следующий час успешно создан!")

    context = {"rundown": rundown_new, "rundown_items": get_times(rundown_new)}

    return render(request, "rundowns/rundown_detail.html", context)


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

    rundown = Rundown.objects.get(id=rundown_news.rundown.id)

    context = {"rundown": rundown, "rundown_items": get_times(rundown)}

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

    rundown = Rundown.objects.get(id=rundown_news.rundown.id)

    context = {"rundown": rundown, "rundown_items": get_times(rundown)}

    return render(request, "rundowns/components/rundown_ul.html", context)
