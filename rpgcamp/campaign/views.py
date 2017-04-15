from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from campaign.forms import CampaignForm, AddUserForm
from campaign.models import Campaign, CampaignUser
from django.contrib.auth.decorators import login_required


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

    context['campaign'] = campaign

    return render(request, 'campaign.html', context=context)

from django.contrib.auth.models import User
@login_required(login_url='/login/')
def add_player(request, slug): 
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    permission = CampaignUser.objects.filter(campaign=campaign, user=request.user, permission=1)
    if not permission:
        return render(request, 'campaign/add_user_denied.html', context=context)
    context['campaign'] = campaign

    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            user = User.objects.filter(username=username)
            if not user:
                context['message'] = "Usuario "+ username +" nao encontrado"
                form = AddUserForm()
            else:
                camp_user = CampaignUser.objects.filter(campaign=campaign, user=user[0])
                if not camp_user:
                    player = CampaignUser(campaign=campaign, user=user[0],permission=2)
                    player.save()
                    context['message'] = "Usuario "+ username +" cadastrado!"
                    form = AddUserForm()
                else:
                    context['message'] = "Usuario "+ username +" ja estava cadastrado!"
                    form = AddUserForm()
    else:
        form = AddUserForm()
    
    context['form'] = form
    return render(request, 'campaign/add_user_campaign.html', context=context)
