from campaign.models import *
from captcha.fields import ReCaptchaField
from django import forms 
class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign 
        fields = ['name','system','description','private']
        labels = {
            'name': 'Nome da Campanha',
            'system': 'Sistema Utilizado',
            'description': 'Descrição da Campanha',
            'private': 'Privado'
        }
        help_texts = {
            'name': 'Escolha com cuidado! O nome da sua campanha irá definir o link para acessar a campanha, e não pode ser alterado no futuro.',
            'private': 'Deixar sua campanha privada irá fazer com que apenas você e seus jogadores possam visualizar a campanha.'        
        }
class AddUserForm(forms.Form):
    user = forms.CharField(label='Nome de Usuário', max_length=100)

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date', 'notes', 'local']
        labels = {
            'date': 'Data da Sessão',
            'notes': 'Observações',
            'local': 'Local do Jogo',
        }
        help_texts = {
            'notes': 'Opcional',
            'local': 'Opcional',
        }
        widgets = {
            'notes': forms.Textarea(attrs={'data-provide': 'markdown'}),
            'local': forms.Textarea(attrs={'data-provide': 'markdown'}),
        }

class ParticipationForm(forms.ModelForm):
    class Meta:
        model = SessionUser
        fields = ['status', 'note']
        labels = {
            'status': 'Opção    ',
            'note': 'Observações',
        }
        help_texts = {
            'note': 'Opcional',
        }

class HouseRulesForm(forms.ModelForm):
    class Meta:
        model = HouseRules
        fields = ['text', 'gm_only_text']
        labels = {
            'text': 'House Rules',
            'gm_only_text': 'Texto Secreto'
        }
        help_texts = {
            'gm_only_text': 'Tudo que você digitar aqui não poderá ser visto pelos jogadores. Você pode utilizar como esboço, ou com anotações para o futuro, por exemplo.'
        }
        widgets = {
            'text': forms.Textarea(attrs={'data-provide': 'markdown'}),
            'gm_only_text': forms.Textarea(attrs={'data-provide': 'markdown'}),
        }

