from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from jinja2 import Environment, FileSystemLoader, select_autoescape
from election2000.regions import GminaRegion, DistrictRegion, VoivodeshipRegion, CountryRegion
from election2000.models import Circuit, Candidate, Votes, Gmina, District
from election2000.forms import UserForm, UploadForm, SearchForm
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
    circ = Circuit.objects.get(district__number = int(district),
            gmina__name = gmina, number = int(circuit))
    votes = Votes.objects.filter(circuit = circ)
    if request.method == "POST":
        for vote in votes:
            vote.number = int(request.POST.get(str(vote.pk)))
            vote.save()
        return HttpResponseRedirect('/Polska/' + '/'.join([voivodeship,
            district, gmina]) + '/')

    else:
        candidates = get_candidates(votes)

    return render(request, 'circuit.html', {'candidates': candidates})

def get_candidates(votes):
    candidates = []
    for vote in votes:
        candidates.append({
            'first_name': vote.candidate.first_name,
            'last_name': vote.candidate.last_name,
            'id': vote.pk,
            'votes': vote.number
        })
    return candidates

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

@login_required
def upload(request, voivodeship, district, gmina, circuit):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            circ = Circuit.objects.get(district__number = int(district),
                    gmina__name = gmina, number = int(circuit))
            circ.document = request.FILES['document']
            circ.save()
            gmina_path = '/'.join(request.path.split('/')[0:-3]) + '/'
            return redirect(gmina_path)
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})

def search_results(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            gminas = []
            for gm in Gmina.objects.filter(name__icontains = query):
                for district in District.objects.filter(circuit__gmina = gm).distinct():
                    gminas.append({
                        'name': gm.name,
                        'url': reverse(gmina, args = [district.voivodeship.name,
                            str(district.number), gm.name])
                    })

            return render(request, 'search_results.html', { 'gminas': gminas })

def save_circuit(circuit, data):
    circuit.eligible = data['eligible']
    circuit.ballots_given_out = data['ballots_given_out']
    circuit.ballots_valid = data['ballots_valid']
    circuit.save()

def save_votes(votes, data):
    votes.number = data['number']
    votes.save()

def render_region(request, region):
    form = SearchForm()
    return render(request, region.template, { 'request': request, 'region': region, 'form': form })
