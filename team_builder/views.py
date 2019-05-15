from django.shortcuts import render
from django.views.generic import ListView

from projects.models import Project, Position


class IndexView(ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = 'projects'
