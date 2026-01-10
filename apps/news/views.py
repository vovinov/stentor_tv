from django.shortcuts import render

from .models import News
from apps.rundowns.models import Rundown

def get_index(request):
    news = News.objects.all()
    rundowns = Rundown.objects.all()
    return render(request, "rundowns/rundown.html", context={"news":news, "rundowns": rundowns})
