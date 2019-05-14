from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .models import Project, Position
from .forms import PositionEditForm, ProjectEditForm, PositionFormSet


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project.html'


class NewProjectView(CreateView):
    model = Project
    form_class = ProjectEditForm
    template_name = 'projects/project_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = PositionFormSet(
            queryset=Position.objects.none()
        )
        return context
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(self.request.POST)
        formset = PositionFormSet(
            self.request.POST,
            queryset=Position.objects.none()
        )

        if form.is_valid():
            project = form.save(commit=False)
            project.user = self.request.user
            project.save()
            if formset.is_valid():
                positions = formset.save(commit=False)
                for position in positions:
                    position.project = project
                    position.user = self.request.user
                    position.save()
                formset.save_m2m()
        return HttpResponseRedirect(reverse('home'))


class EditProjectView(UpdateView):
    model = Project
    form_class = ProjectEditForm
    template_name = 'projects/project_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = PositionFormSet(
            queryset=Position.objects.filter(project=self.get_object())
        )
        return context
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(self.request.POST, instance=self.get_object())
        formset = PositionFormSet(
            self.request.POST,
            queryset=Position.objects.filter(project=self.get_object())
        )

        if form.is_valid():
            project = form.save(commit=False)
            project.user = self.request.user
            project.save()
            if formset.is_valid():
                Position.objects.filter(project=project).delete()
                positions = formset.save(commit=False)
                for position in positions:
                    position.project = project
                    position.user = self.request.user
                    position.save()
                formset.save_m2m()
            print(formset.errors)
        return HttpResponseRedirect(reverse('projects:project_detail',
                                    kwargs={"pk": project.pk}))


class DeleteProjectView(DeleteView):
    model = Project
    success_url = reverse_lazy('home')
