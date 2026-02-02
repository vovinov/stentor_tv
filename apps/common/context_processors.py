from django.utils import timezone

from apps.rundowns.models import Rundown


def get_last_rundowns(request):
    today = timezone.now()
    rundowns = Rundown.objects.filter(air_day=today.day)[:5]
    return {"rundowns": rundowns}