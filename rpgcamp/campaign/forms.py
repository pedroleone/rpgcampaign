from campaign.models import Campaign 
from captcha.fields import ReCaptchaField
from django import forms 
class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign 
        fields = ['name','system','description','private']

class AddUserForm(forms.Form):
    user = forms.CharField(label='Nome de Usuário', max_length=100)

