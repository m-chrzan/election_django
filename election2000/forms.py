from django.forms import ModelForm
from election2000.models import Circuit, Votes

class CircuitForm(ModelForm):
    class Meta:
        model = Circuit
        fields = ['eligible', 'ballots_given_out', 'ballots_valid']
