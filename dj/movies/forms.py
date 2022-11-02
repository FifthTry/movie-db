from django import forms


class SearchForm(forms.Form):
    title = forms.CharField(label="title", max_length=100, required=True)
