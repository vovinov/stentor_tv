from django.utils import timezone
from datetime import time

from apps.rundowns.models import Rundown


def round_to_hour(dt):

    seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    rounded_seconds = round(seconds / 3600.0) * 3600
    return dt.replace(hour=rounded_seconds // 3600, minute=0, second=0, microsecond=0)


def get_air_date():
    today = timezone.localtime()

    curremt_day = today.day
    curremt_year = today.year
    current_month = today.month


def add_time(start_time, duration):
    total_seconds = (
        start_time.hour * 3600
        + start_time.minute * 60
        + start_time.second
        + duration.total_seconds()
    )

    # Модульно по 24 часам (86400 секунд в сутках)
    total_seconds = total_seconds % 86400

    # Из секунд получаем часы, минуты, секунды
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    return time(hours, minutes, seconds)


def get_times(rundown):

    start_time = time(rundown.air_hour, 0, 0)
    end_time = time(rundown.air_hour, 0, 0)

    rundown_items = []

    for pos, r in enumerate(rundown.rundown_news.all(), 1):  # type: ignore

        if r.news.asset:
            r.rundown.duration += r.news.asset.duration
            end_time = add_time(start_time, r.news.asset.duration)
        else:
            end_time = start_time

        rundown_items.append(
            {"item": r, "time": {"start_time": start_time, "end_time": end_time}}
        )

        start_time = end_time

    return rundown_items
