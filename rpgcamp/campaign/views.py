from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from campaign.forms import CampaignForm
from campaign.models import Campaign, CampaignUser
from django.contrib.auth.decorators import login_required

def index(request):
    context = {}
    if request.user.is_authenticated:
        campaign_list = CampaignUser.objects.filter(user=request.user)
        context['campaign_list'] = campaign_list
    return render(request, 'index.html', context=context)

@login_required(login_url='/login/')
def create_campaign(request):
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save()
            campaign_user = CampaignUser(user = request.user, campaign=campaign, permission=1)
            campaign_user.save()
            return HttpResponseRedirect('/')
    else:
        form = CampaignForm()
    context = {'form': form}
    return render(request, 'campaign/create_campaign.html', context)
    
@login_required(login_url='/login/')
def view_campaign(request, slug):
    context = {}

    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.private is True:
        permission = CampaignUser.objects.filter(campaign=campaign, user=request.user)
        if not permission:
            return render(request, 'campaign_denied.html', context=context)

    context['campaign'] = campaign

    return render(request, 'campaign.html', context=context)