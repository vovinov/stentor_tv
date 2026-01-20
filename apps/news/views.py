from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect

from apps.rundowns.models import Rundown, RundownNews

from .models import News


def news_create(request):

    title = request.POST.get("title")
    content = request.POST.get("content")

    news = News.objects.create(title=title, content=content)

    rundown = Rundown.objects.all().first()

    last_pos = (
        RundownNews.objects.filter(rundown=rundown)
        .order_by("-position")
        .values_list("position", flat=True)
        .first()
        or 0
    )

    RundownNews.objects.get_or_create(
        rundown=rundown, news=news, defaults={"position": last_pos + 1}
    )

    return redirect(
        "index",
    )


def news_delete(request, item_id):

    RundownNews.objects.get(id=item_id).delete()

    return redirect(
        "index",
    )
