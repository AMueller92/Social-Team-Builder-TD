from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Profile, Skill, SelfChoosenSkill
from .forms import ProfileEditForm, SkillFormSet
from projects.models import Project


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def user_profile(request):
    profile = request.user.profile
    projects = Project.objects.filter(user=request.user)
    return render(
        request,
        'accounts/profile.html',
        {'object': profile, 'projects': projects}
    )


def any_user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    projects = Project.objects.filter(user=profile.user)
    return render(
        request,
        'accounts/profile.html',
        {'object': profile, 'projects': projects}
    )


def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES,
                                       instance=request.user.profile)
        formset = SkillFormSet(request.POST,
                               queryset=SelfChoosenSkill.objects.filter(profile=request.user.profile))

        if profile_form.is_valid():
            profile = profile_form.save()
            if formset.is_valid():
                SelfChoosenSkill.objects.filter(profile=profile).delete()
                skills = formset.save(commit=False)
                for skill in skills:
                    skill.profile = profile
                    skill.save()
                messages.success(
                    request,
                    "You edited your profile!"
                )
                return HttpResponseRedirect(reverse('accounts:profile'))

    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        formset = SkillFormSet(queryset=SelfChoosenSkill.objects.filter(profile=request.user.profile))

    context = {
        'profile_form': profile_form,
        'formset': formset,
        'object': profile,
    }

    return render(request, 'accounts/profile_edit.html', context)
