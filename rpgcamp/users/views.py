from django.shortcuts import render
from users.forms import UserForm, UserProfileForm
from django.contrib.auth import login 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Profile

def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'] )

            login(request, new_user)
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
        
    return render(request, 'registration/add_user.html', {'form': form})

def profile(request):
    try:
        initial_profile = Profile.objects.get(user=request.user)
    except:
        initial_profile = Profile(user=request.user, display_name=request.user.username)
    print(initial_profile.display_name)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        form.user = request.user
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.id = initial_profile.id
            profile.save()
            return HttpResponseRedirect('/')
    else:
        form = UserProfileForm(instance=initial_profile)
        
    return render(request, 'profile.html', {'form': form})