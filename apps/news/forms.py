from django import forms
from datetime import timedelta

from apps.news.models import News

class NewsCreateForm(forms.ModelForm):
    # параметры для добавления в rundown
    rundown_id = forms.IntegerField(required=True)
    position = forms.IntegerField(required=False, min_value=0, initial=0)
    duration_seconds = forms.IntegerField(required=False, min_value=0, initial=0)

    class Meta:
        model = News
        fields = ["title", "content", "status"]