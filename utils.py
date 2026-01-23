from django.utils import timezone


def round_to_hour(dt):

    seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    rounded_seconds = round(seconds / 3600.0) * 3600
    return dt.replace(hour=rounded_seconds // 3600, minute=0, second=0, microsecond=0)


def get_air_date():
    today = timezone.localtime()

    curremt_day = today.day
    curremt_year = today.year
    current_month = today.month
