from django.forms import ModelForm
from campaign.models import Campaign 
from captcha.fields import ReCaptchaField

class CampaignForm(ModelForm):
    class Meta:
        model = Campaign 
        fields = ['name','system','description','private']
