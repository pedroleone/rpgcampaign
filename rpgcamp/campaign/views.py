from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from campaign.forms import *
from campaign.models import *

from django.utils import timezone
from datetime import datetime

def get_campaigns(request):
    if request.user.is_authenticated:
        return CampaignUser.objects.filter(user=request.user)


def index(request):
    campaign_list = get_campaigns(request)
    context = { 'campaign_list': campaign_list }
    return render(request, 'index.html', context=context)


@login_required(login_url='/login/')
def create_campaign(request):
    context = { 'campaign_list': get_campaigns(request) }
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save()
            campaign_user = CampaignUser(user = request.user, campaign=campaign, permission=1)
            campaign_user.save()
            return HttpResponseRedirect('/')
    else:
        form = CampaignForm()
    context['form'] = form
    return render(request, 'campaign/create_campaign.html', context)
    

def view_campaign(request, slug):
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.private is True:
        permission = CampaignUser.objects.filter(campaign=campaign, user=request.user)
        if not permission:
            return render(request, 'campaign_denied.html', context=context)
    session = Session.objects.filter(campaign=campaign, date__gte=timezone.now())
    if session:
        next_session = session[0]
        context['next_session'] = next_session

    context['campaign'] = campaign
    return render(request, 'campaign.html', context=context)


from django.contrib.auth.models import User
@login_required(login_url='/login/')
def players(request, slug): 
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    permission = CampaignUser.objects.filter(campaign=campaign, user=request.user, permission=1)
    if not permission:
        context['add_user_permission'] = False
    else:
        context['add_user_permission'] = True
    context['campaign'] = campaign
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            user = User.objects.filter(username=username)
            if not user:
                alert = {
                    'title': "Erro!",
                    'type': "danger",
                    'message': "Usuário <strong>"+ username +"</strong> não encontrado",
                }
                context['alert'] = alert
                form = AddUserForm()
            else:
                camp_user = CampaignUser.objects.filter(campaign=campaign, user=user[0])
                if not camp_user:
                    player = CampaignUser(campaign=campaign, user=user[0],permission=2)
                    player.save()
                    future_sessions = Session.objects.filter(campaign=campaign, date__gte=timezone.now()).first()
                    if future_sessions:
                        future_sessions.save()
                    alert = {
                        'title': "Sucesso!",
                        'type': "success",
                        'message': "Usuário <strong>"+ username +"</strong> cadastrado",
                    }
                    context['alert'] = alert                    
                    form = AddUserForm()
                else:
                    alert = {
                        'title': "Aviso!",
                        'type': "warning",
                        'message': "Usuário <strong>"+ username +"</strong> já estava cadastrado",
                    }
                    context['alert'] = alert    

                    form = AddUserForm()
    else:
        form = AddUserForm()
    context['form'] = form
    return render(request, 'campaign/add_user_campaign.html', context=context)


@login_required(login_url='/login/')
def delete_player(request, slug):
    campaign_id = request.POST.get('delete_campaign_id')
    user_id = request.POST.get('delete_user_id')
    obj = CampaignUser.objects.get(user=user_id, campaign=campaign_id)
    obj.delete()

    future_sessions = Session.objects.filter(campaign=campaign_id, date__gte=timezone.now()).first()
    if future_sessions:
        future_sessions.save()

    return HttpResponseRedirect(reverse('players', args=[slug]))


@login_required(login_url='/login/')
def new_session(request, slug):
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            session = Session(campaign=campaign, 
                              date=form.cleaned_data['date'],
                              local=form.cleaned_data['local'],
                              notes=form.cleaned_data['notes'])
            session.save()
            return HttpResponseRedirect(reverse('view_campaign', args=[campaign.slug])) 
    else:
        form = SessionForm()
    context['campaign'] = campaign
    context['form'] = form
    return render(request, 'session/new_session.html', context=context)


@login_required(login_url='/login/')            
def view_sessions(request, slug):
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    context['campaign'] = campaign
    session = Session.objects.filter(campaign=campaign, date__gte=timezone.now())
    if session:
        next_session = session[0]
        context['next_session'] = next_session
        if session.count() > 1:
            future_sessions = session[1:]
            context['future_sessions'] = future_sessions
    context['old_sessions'] = Session.objects.filter(campaign=campaign, date__lt=timezone.now())
    session = Session.objects.filter(campaign=campaign, date__gte=timezone.now())
    if session:
        context['next_session'] = next_session
    return render(request, 'session/view_sessions.html', context=context)


@login_required(login_url='/login/')
def view_session(request, slug, session_id):
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    session = get_object_or_404(Session, id=session_id, campaign=campaign)
    context['campaign'] = campaign
    context['session'] = session
    return render(request, 'session/view_session.html', context=context)
    

@login_required(login_url='/login/')
def edit_session(request, slug, session_id):
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    session = get_object_or_404(Session, id=session_id, campaign=campaign)
    initial_data = {
        'date': session.date,
        'local': session.local,
        'notes': session.notes
    }
    form = SessionForm(initial_data)
    print(request.POST)
    if request.method == "POST":
        method = request.POST.get('action')
        if method == 'delete':
            session.delete()
            return HttpResponseRedirect(reverse('view_sessions', args=[campaign.slug])) 
        form = SessionForm(request.POST)
        if form.is_valid():
            session = Session(id=session.id,
                              campaign=campaign, 
                              date=form.cleaned_data['date'],
                              local=form.cleaned_data['local'],
                              notes=form.cleaned_data['notes'])
            session.save()
            return HttpResponseRedirect(reverse('view_sessions', args=[campaign.slug])) 

    context['campaign'] = campaign
    context['form'] = form
    return render(request, 'session/edit_session.html', context=context)

def session_participation(request, slug, session_id):
    context = { 'campaign_list': get_campaigns(request) }
    action = request.POST.get('action')
    next_page = request.POST.get('redirect')
    user_id = request.POST.get('user_id')
    campaign = get_object_or_404(Campaign, slug=slug)
    session = get_object_or_404(Session, id=session_id, campaign=campaign)
    session_user = get_object_or_404(SessionUser, 
                                     user=user_id, 
                                     campaign=campaign, 
                                     session=session)

    print(next_page)
    if action == "confirm-yes":
        session_user.status = 3
        session_user.save()
        redirect = True
    elif action == "confirm-no":
        session_user.status = 2
        session_user.save()
        redirect = True
    elif action == "confirm-not-yet":
        session_user.status = 4
        session_user.save()
        redirect = True

    if redirect:
        if next_page=="main":
            #HttpResponseRedirect(reverse('view_campaign', args=[slug])) 
            return HttpResponseRedirect(reverse('view_campaign', args=[slug])) 
        else:
            return HttpResponseRedirect(reverse('view_session', args=[slug, session.id])) 
            
    

    return render(request, 'session/edit_participation.html', context=context)
