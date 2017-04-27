from django import forms
from election2000.models import Circuit, Votes
from django.contrib.auth.models import User

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

class UploadForm(forms.Form):
    document = forms.FileField(label = "Dokument")

class SearchForm(forms.Form):
    query = forms.CharField(label = "Szukaj gminy")
