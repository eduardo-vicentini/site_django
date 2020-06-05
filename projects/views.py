from django.shortcuts import render
from django.views import generic
from .models import Project

class ProjectList(generic.ListView):
    queryset = Project.objects.all()
    template_name = 'index_projects.html'
    paginate_by = 6