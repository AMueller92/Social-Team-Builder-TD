from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Profile


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
