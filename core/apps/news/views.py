from django.http import HttpResponse
from django.shortcuts import render

from .models import News


# Create your views here.
def render_index(request):
    news = News.objects.all()
    return render(request, 'news/news.html', context={'news': news})