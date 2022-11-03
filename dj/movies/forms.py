from django import forms
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SearchForm(forms.Form):
    title = forms.CharField(label="title", max_length=1024, required=True)


class ReviewForm(forms.Form):
    rating = forms.IntegerField(label="rating", required=True, error_messages={
        'required': "Please Enter value between 1 and 10"},
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    reviewer = forms.CharField(label="reviewer", max_length=1024, required=True, error_messages={
        'required': "Please Enter your name"})
    title = forms.CharField(label="title", max_length=1024, required=True)
    description = forms.CharField(label="description", required=True)
