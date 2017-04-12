from django.shortcuts import render
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
    