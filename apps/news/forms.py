from django import forms

from apps.news.models import News


class NewsEditForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ["title", "content"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["title"].widget.attrs.update({"class": "form-control"})
    #     self.fields["content"].widget.attrs.update(
    #         {"class": "form-control", "rows": 10}
    #     )

    # # В NewsEditForm добавьте:
    # def get_form(self):
    #     form = super().get_form()
    #     print("FORM VALUES:", form.cleaned_data if form.is_valid() else "NOT VALID")
    #     return form
