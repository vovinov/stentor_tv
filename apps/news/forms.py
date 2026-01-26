from django import forms

from apps.news.models import News


class NewsCreationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input input-bordered w-full"})
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "input input-bordered w-full", "row": "20"}
        )
    )

    class Meta:
        model = News
        fields = ("title", "content")


class NewsEditForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input input-bordered w-full"})
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "input input-bordered w-full", "row": "20"}
        )
    )

    class Meta:
        model = News
        fields = ["title", "content"]
