from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from jinja2 import Environment, FileSystemLoader, select_autoescape
from election2000.regions import GminaRegion, DistrictRegion, VoivodeshipRegion, CountryRegion
from election2000.models import Circuit, Candidate, Votes
from election2000.forms import CircuitForm, VotesForm, UserForm
from django.template import loader

def country(request):
    return render_region(request, CountryRegion())

def voivodeship(request, voivodeship):
    return render_region(request, VoivodeshipRegion(voivodeship))

def district(request, voivodeship, district):
    return render_region(request, DistrictRegion(district))

def gmina(request, voivodeship, district, gmina):
    return render_region(request, GminaRegion(gmina, district))

@login_required
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

@login_required
def candidate(request, voivodeship, district, gmina, circuit, candidate):
    first_name = ' '.join(candidate.split()[0:-1])
    last_name = candidate.split()[-1]
    votes = Votes.objects.get(candidate__first_name = first_name,
            candidate__last_name = last_name, circuit__number = int(circuit),
            circuit__gmina__name = gmina,
            circuit__district__number = int(district))

    if request.method == "POST":
        form = VotesForm(request.POST)
        if form.is_valid():
            save_votes(votes, form.cleaned_data)
            return HttpResponseRedirect('/Polska/' + '/'.join([voivodeship,
                district, gmina]) + '/')
    else:
        form = VotesForm(instance = votes)

    return render(request, 'votes.html', {'form': form, 'votes': votes})

def login_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')
                return redirect(next_page)
    else:
        form = UserForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    next = request.GET.get('next')
    return redirect(next)


def save_circuit(circuit, data):
    circuit.eligible = data['eligible']
    circuit.ballots_given_out = data['ballots_given_out']
    circuit.ballots_valid = data['ballots_valid']
    circuit.save()

def save_votes(votes, data):
    votes.number = data['number']
    votes.save()

def render_region(request, region):
    return render(request, region.template, { 'request': request, 'region': region })
