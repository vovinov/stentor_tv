from django.utils import timezone
from datetime import time


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
