#from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView

from projects.models import Project


class IndexView(TemplateView):
    template_name = "projects/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context
