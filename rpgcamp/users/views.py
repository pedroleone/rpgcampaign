from django.shortcuts import render, get_object_or_404
from users.forms import UserForm, UserProfileForm, UserProfileNewForm
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

def add_user_profile(request):
    if request.method == "POST":
        form = UserProfileNewForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'] )

            login(request, new_user)
            profile = Profile(user=request.user, 
                              display_name=form.cleaned_data['display_name'],
                              home_city=form.cleaned_data['home_city'],
                              bio=form.cleaned_data['bio'],
                              facebook=form.cleaned_data['facebook'],
                              twitter=form.cleaned_data['twitter'],)
            profile.save()
            return HttpResponseRedirect('/')
    else:
        form = UserProfileNewForm()
        
    return render(request, 'registration/add_user_profile.html', {'form': form})


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
            if form.cleaned_data['profile_pic'] is None:
                profile.profile_pic = initial_profile.profile_pic
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
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    if request.user == user:
        return HttpResponseRedirect('/profile/')
    
    context['profile'] = profile
    context['user'] = user
    return render(request, 'users/view_profile.html', context)
