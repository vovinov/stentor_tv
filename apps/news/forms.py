from django import forms

from apps.news.models import News
from django.contrib.auth.models import Group

from apps.statuses.models import Status


class NewsCreationForm(forms.ModelForm):
    title = forms.CharField(
        label="Название новости",
        widget=forms.TextInput(attrs={"class": "input input-bordered w-full"}),
    )
    content = forms.CharField(
        label="Текст новости",
        widget=forms.Textarea(attrs={"class": "textarea w-full"}),
    )
    editor = forms.ModelChoiceField(
        queryset=Group.objects.get(name="editor").user_set.all(),
        widget=forms.Select(attrs={"class": " w-full select"}),
        empty_label="Выберите редактора",
        label="Редактор",
        required=False,
    )

    class Meta:
        model = News
        fields = ("title", "content", "editor")


class NewsEditForm(forms.ModelForm):
    title = forms.CharField(
        label="Название", widget=forms.TextInput(attrs={"class": "p-2 input w-full"})
    )
    content = forms.CharField(
        label="Текст новости", widget=forms.Textarea(attrs={"class": "textarea w-full"})
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.exclude(title="Создано"),
        widget=forms.Select(attrs={"class": "w-full select status-changer"}),
        empty_label="Выберите статус",
        label="Статус",
    )
    comment = forms.CharField(
        label="Комментарий", 
        widget=forms.Textarea(attrs={
                "class": "input input-bordered w-full h-auto",
                'disabled': True,
                "rows": 5,
                "cols": 50,
            }),
        required=False
    )

    class Meta:
        model = News
        fields = ["title", "content", "status", "comment"]


class NewsAddCommentForm(forms.Form):

    comment = forms.CharField(
        label="Комментарий",
        widget=forms.Textarea(
            attrs={
                "class": "input input-bordered w-full h-auto",
                "rows": 15,
                "cols": 50,
            }
        ),
    )
