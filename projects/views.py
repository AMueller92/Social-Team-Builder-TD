from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from notifications.signals import notify

from .models import Project, Position, Application
from .forms import PositionEditForm, ProjectEditForm, PositionFormSet


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = Position.objects.filter(
            project=context['object']).exclude(applications__status='A')
        context['applied'] = Position.objects.filter(project=context['object'],
                                                     applications__applicant=self.request.user)
        return context


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


def position_apply(request, position_pk):

    position = Position.objects.get(id=position_pk)
    project = position.project
    application = Application.objects.filter(applicant=request.user, position=position)

    if application.exists():
        return HttpResponseRedirect(reverse('projects:project_detail',
                                    kwargs={"pk": project.pk}))

    Application.objects.create(applicant=request.user, position=position)

    notify.send(
        request.user,
        recipient=request.user,
        verb=f"You applied to {position.name} for the project {project.title}"
    )

    notify.send(
        request.user,
        recipient=project.user,
        verb=f"{request.user} applied to the Positon: {position.name} for Project: {project.title}"
    )

    return HttpResponseRedirect(reverse('home'))


def notifications_view(request):
    unread_notifs = request.user.notifications.unread()
    return render(request, 'projects/notifications.html', {'unread_notifs': unread_notifs})


def applications_view(request):
    applications = Application.objects.filter(position__project__user=request.user)
    return render(request, 'projects/applications.html', {'applications': applications})


def application_status_view(request, application_pk, status):
    application = Application.objects.get(id=application_pk)
    position = Position.objects.get(applications__id=application.id)

    if status == "accepted":
        application.status = "A"
        application.save()

        notify.send(
            request.user,
            recipient=application.applicant,
            verb=f"You are accepted for the Position: {application.position} of Project: {application.position.project}"
        )
        notify.send(
            request.user,
            recipient=request.user,
            verb=f"You accepted {application.applicant} for the Position: {application.position}"
        )
    
    if status == "rejected":
        application.status = "R"
        application.save()

        notify.send(
            request.user,
            recipient=application.applicant,
            verb=f"You got rejected for the Position: {application.position} of Project: {application.position.project}"
        )
        notify.send(
            request.user,
            recipient=request.user,
            verb=f"You rejected {application.applicant} for the Position: {application.position}"
        )
    
    return HttpResponseRedirect(reverse('projects:applications'))


def search(request):
    search_term = request.GET.get('search_box', None)
    projects = Project.objects.filter(
        Q(title__icontains=search_term) |
        Q(description__icontains=search_term)
    )
    return render(request, "projects/index.html", {'projects': projects})


def skill_search(request, skill):
    projects = Project.objects.filter(positions__skills__name=skill)
    return render(request, "projects/index.html", {'projects': projects})
