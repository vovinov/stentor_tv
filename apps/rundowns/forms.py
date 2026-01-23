from django import forms


class RundownsDateForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), label="Дата")


class RundownNewsAddForm(forms.Form):
    rundown = forms.Select()
