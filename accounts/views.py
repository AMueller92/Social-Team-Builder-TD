from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Profile
from .forms import ProfileEditForm


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

# TODO später benutzt um alle profile anzuzeigen
#class ProfileDetailView(DetailView):
#    model = Profile
#    template_name = 'accounts/profile.html'


def user_profile(request):
    profile = request.user.profile
    skills = profile.skills.all()
    return render(
        request,
        'accounts/profile.html',
        {'object': profile, 'skills': skills}
    )


def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES,
                                       instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(
                request,
                "You edited your profile!"
            )
            return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'profile_form': profile_form,
        'object': profile
    }

    return render(request, 'accounts/profile_edit.html', context)
