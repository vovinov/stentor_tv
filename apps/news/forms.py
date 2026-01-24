from django import forms

from apps.news.models import News


class NewsCreationForm(forms.ModelForm):
    title = forms.CharField(
        widget=TextInput(attrs={"class": "input input-bordered w-full"})
    )
    content = forms.Textarea(widget=Area)

    class Meta:
        model = News
        fields = ["title", "content"]


class NewsEditForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ["title", "content"]
