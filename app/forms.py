from django import forms
from .models import *
from django.db import models


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body',]


class SearchForm(forms.Form):
    query = forms.CharField()
