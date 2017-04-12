from django.shortcuts import render
from users.forms import UserForm
from django.contrib.auth import login 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)


            login(request, new_user)
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
        
    return render(request, 'registration/add_user.html', {'form': form})