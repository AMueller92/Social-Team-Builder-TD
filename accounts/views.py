from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Profile, Skill, SelfChoosenSkill, UserProject
from .forms import ProfileEditForm, SkillFormSet, UserProjectFormSet
from projects.models import Project


@login_required
def user_profile(request):
    profile = request.user.profile
    projects = Project.objects.filter(user=request.user)
    attempted_projects = Project.objects.filter(
        positions__applications__applicant=request.user).exclude(
            positions__applications__status='P').exclude(
                positions__applications__status='R')
    user_projects = UserProject.objects.filter(user=request.user)
    
    context = {'object': profile,
               'projects': projects,
               'attempted_projects': attempted_projects,
               'user_projects': user_projects}

    return render(request, 'accounts/profile.html', context)


@login_required
def any_user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    projects = Project.objects.filter(user=profile.user)
    attempted_projects = Project.objects.filter(
        positions__applications__applicant=profile.user).exclude(
            positions__applications__status='P').exclude(
                positions__applications__status='R')
    user_projects = UserProject.objects.filter(user=profile.user)

    context = {'object': profile,
               'projects': projects,
               'attempted_projects': attempted_projects,
               'user_projects': user_projects}

    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES,
                                       instance=profile)
        formset = SkillFormSet(request.POST,
                               queryset=SelfChoosenSkill.objects.filter(profile=profile))
        #user_project_formset = UserProjectFormSet(request.POST,
         #                                         queryset=UserProject.objects.filter(user=request.user))

        if profile_form.is_valid():
            profile = profile_form.save()
            if formset.is_valid():
                skills = formset.save(commit=False)
                for skill in skills:
                    skill.profile = profile
                    skill.save()
                #if user_project_formset.is_valid():
                 #   print('user project valid')
                   # user_project = user_project_formset.save(commit=False)
                    #for project in user_project:
                     #   project.user = profile.user
                      #  project.save()
            messages.success(
                request,
                "You edited your profile!"
            )
            return HttpResponseRedirect(reverse('accounts:profile'))

    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        formset = SkillFormSet(queryset=SelfChoosenSkill.objects.filter(profile=request.user.profile))
        #user_project_formset = UserProjectFormSet(queryset=UserProject.objects.filter(user=request.user))

    context = {
        'profile_form': profile_form,
        'formset': formset,
        'object': profile,
        #'user_project_formset': user_project_formset,
    }

    return render(request, 'accounts/profile_edit.html', context)
