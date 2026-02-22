from django import forms

from apps.assets.models import Asset


class AssetCreationForm(forms.ModelForm):
    title = forms.CharField(
        label="Название материала",
        widget=forms.TextInput(attrs={"class": "input input-bordered w-full"}),
    )
    duration = forms.DurationField(
        label="Хронометраж",
        widget=forms.TimeInput(attrs={"class": "w-full"}),
    )
    video = forms.FileField(
        label="Файл",
        widget=forms.FileInput(attrs={"class": "file-input w-full"}),
    )


    class Meta:
        model = Asset
        fields = ("title", "duration", "video")
