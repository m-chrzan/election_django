from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from jinja2 import Environment, FileSystemLoader, select_autoescape
from election2000.regions import GminaRegion, DistrictRegion, VoivodeshipRegion, CountryRegion
from election2000.models import Circuit, Candidate, Votes
from election2000.forms import CircuitForm
from django.template import loader

def country(request):
    return render_region(CountryRegion())

def voivodeship(request, voivodeship):
    return render_region(VoivodeshipRegion(voivodeship))

def district(request, voivodeship, district):
    return render_region(DistrictRegion(district))

def gmina(request, voivodeship, district, gmina):
    return render_region(GminaRegion(gmina, district))

def circuit(request, voivodeship, district, gmina, circuit):
    candidates = Candidate.objects.all()
    circ = Circuit.objects.get(district__number = int(district),
            gmina__name = gmina, number = int(circuit))
    if request.method == "POST":
        form = CircuitForm(request.POST)
        if form.is_valid():
            save_circuit(circ, form.cleaned_data)
            return HttpResponseRedirect('/Polska/' + '/'.join([voivodeship,
                district, gmina]) + '/')
    else:
        form = CircuitForm(instance = circ)

    return render(request, 'circuit.html', {'form': form, 'circuit': circuit,
        'candidates': candidates})


def save_circuit(circuit, data):
    circuit.eligible = data['eligible']
    circuit.ballots_given_out = data['ballots_given_out']
    circuit.ballots_valid = data['ballots_valid']
    circuit.save()

def render_region(region):
    template = loader.get_template(region.template)
    rendered = template.render({'region': region})
    return HttpResponse(rendered)
