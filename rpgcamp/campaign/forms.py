from django.forms import ModelForm
from campaign.models import Campaign 

class CampaignForm(ModelForm):
    class Meta:
        model = Campaign 
        fields = ['name','system','description']
