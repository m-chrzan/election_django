from django.shortcuts import render
from django.http import HttpResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from election2000.regions import GminaRegion, DistrictRegion, VoivodeshipRegion, CountryRegion
from django.template import loader

def country(request):
    return render_region(CountryRegion())

def render_region(region):
    template = loader.get_template(region.template)
    rendered = template.render({'region': region})
    return HttpResponse(rendered)
