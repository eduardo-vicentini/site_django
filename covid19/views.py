from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView

class CovidDetail(TemplateView):
    template_name = 'covid.html'
