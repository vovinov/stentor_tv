from django.shortcuts import render, redirect

from .models import News
from apps.statuses.models import Status

def create_news(request):

    title = request.POST.get("title")
    content = request.POST.get("content")
    status = Status.objects.get(title="Создано")

    news, created = News.objects.get_or_create(
            title=title,
            defaults={"content": content, "status": status},
        )
    
    if not created:
        return render(request, 
            "rundowns/rundown.html", {
            "error_modal": True,
            "error_text": "Новость с таким заголовком уже существует.",
            "title_value": title,
            "content_value": content,
        })

    return redirect("rundown_get_last")
    
