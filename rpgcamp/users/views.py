from django.shortcuts import render, get_object_or_404
from users.forms import UserForm, UserProfileForm
from django.contrib.auth import login 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Profile

from django.contrib.auth.decorators import login_required
from campaign.views import get_campaigns

def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'] )

            login(request, new_user)
            profile = Profile(user=request.user, display_name=request.user.username)
            profile.save()
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
        
    return render(request, 'registration/add_user.html', {'form': form})

@login_required(login_url='/login/')
def edit_profile(request):
    context = { 'campaign_list': get_campaigns(request) }
    try:
        initial_profile = Profile.objects.get(user=request.user)
    except:
        initial_profile = Profile(user=request.user, display_name=request.user.username)
        initial_profile.save()
    print(initial_profile.display_name)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        form.user = request.user
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.id = initial_profile.id
            profile.save()
            return HttpResponseRedirect('/profile/')
    else:
        form = UserProfileForm(instance=initial_profile)
    context['form'] = form
    return render(request, 'users/edit_self_profile.html', context)

@login_required(login_url='/login/')
def self_profile(request):
    context = { 'campaign_list': get_campaigns(request) }
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = Profile(user=request.user, display_name=request.user.username)
        profile.save()
    context['profile'] = profile
    return render(request, 'users/view_self_profile.html', context)

def view_profile(request, username):
    context = { 'campaign_list': get_campaigns(request) }
    profile = get_object_or_404(Profile, user=username)
    context['profile'] = profile
    return render(request, 'users/view_profile.html', context)
