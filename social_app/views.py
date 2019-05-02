from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Project, Profile


class ProjectListView(ListView):
    model = Project
    template_name = 'social_app/index.html'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'social_app/project.html'


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'social_app/profile.html'
