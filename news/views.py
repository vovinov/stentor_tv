from django.shortcuts import render


def news_view(request):
	return render(request, 'news/index.html')
