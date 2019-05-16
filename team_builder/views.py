from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from projects.models import Project, Position


class IndexView(ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = Position.objects.exclude(applications__status='A')
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()

        search_term = self.request.GET.get('search_box', None)
        if search_term:
            queryset = queryset.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(positions__name__icontains=search_term))

        position_key = self.request.GET.get('position')
        if position_key:
            queryset = queryset.filter(positions__name=position_key)
        
        match_skill = self.request.GET.get('skill')
        if match_skill:
            skills = self.request.user.profile.skills.all()
            queryset = queryset.filter(positions__skills__in=skills).distinct()

        return queryset
