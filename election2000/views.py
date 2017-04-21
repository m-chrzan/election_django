from django.shortcuts import render
from django.http import HttpResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from election2000.regions import GminaRegion, DistrictRegion, VoivodeshipRegion, CountryRegion
from django.template import loader

def country(request):
    return render_region(CountryRegion())

def voivodeship(request, voivodeship):
    return render_region(VoivodeshipRegion(voivodeship))

def district(request, voivodeship, district):
    return render_region(DistrictRegion(district))

def gmina(request, voivodeship, district, gmina):
    return render_region(GminaRegion(gmina, district))

def render_region(region):
    template = loader.get_template(region.template)
    rendered = template.render({'region': region})
    return HttpResponse(rendered)
