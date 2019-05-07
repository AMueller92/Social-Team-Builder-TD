from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Project


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project.html'
