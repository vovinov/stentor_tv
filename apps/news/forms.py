from django import forms

from apps.news.models import News
from django.contrib.auth.models import Group


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

    class Meta:
        model = News
        fields = ["title", "content"]


class NewsStatusChangeForm(forms.Form):

    CHOICES = [
        ("Текст", "Текст"),
        ("Монтаж", "Монтаж"),
        ("Эфир", "Эфир"),
        ("Правка", "Правка"),
    ]

    status = forms.ChoiceField(
        label="Статус",
        choices=CHOICES,
        widget=forms.Select(attrs={"class": "input input-bordered w-full"}),
    )
    comment = forms.CharField(
        label="Комментарий",
        widget=forms.Textarea(
            attrs={"class": "input input-bordered w-full", "cols": "2", "rows": "20"}
        ),
    )
