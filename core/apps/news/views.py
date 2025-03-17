from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def render_index(request):
    return HttpResponse('Hello, world')