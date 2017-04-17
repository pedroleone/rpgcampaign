from campaign.models import *
from captcha.fields import ReCaptchaField
from django import forms 
class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign 
        fields = ['name','system','description','private']

class AddUserForm(forms.Form):
    user = forms.CharField(label='Nome de Usuário', max_length=100)

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date', 'notes', 'local']
        labels = {
            'date': 'Date',
            'notes': 'Observações',
            'local': 'Local do Jogo',
        }
        help_texts = {
            'notes': 'Você pode usar <a href="http://daringfireball.net/projects/markdown/">Markdown</a> para formatar o texto.',
            'local': 'Você pode usar <a href="http://daringfireball.net/projects/markdown/">Markdown</a> para formatar o texto.',
        }
