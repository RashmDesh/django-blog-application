from django import forms

from django.contrib.auth.models import User
from login.models import bloguser

choices= [
    ('education', 'Education'),
    ('politics', 'Politics'),
    ('medical', 'Medical'),
    ('sports', 'Sports'),
    ('games', 'Games'),
    ('entertainment', 'Entertainment')
    ]


class Blogform(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(widget=forms.Textarea)
    created_on = forms.DateTimeField()
    category = forms.CharField(widget=forms.Select(choices=choices))
    file = forms.FileField()