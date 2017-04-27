from django import forms
from election2000.models import Circuit, Votes
from django.contrib.auth.models import User

class CircuitForm(forms.ModelForm):
    class Meta:
        model = Circuit
        fields = ['eligible', 'ballots_given_out', 'ballots_valid']

class VotesForm(forms.ModelForm):
    class Meta:
        model = Votes
        fields = ['number']

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

class UploadForm(forms.Form):
    document = forms.FileField(label = "Dokument")

class SearchForm(forms.Form):
    query = forms.CharField(label = "Szukaj gminy")
