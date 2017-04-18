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
            'notes': 'Opcional. Você pode usar <a href="http://daringfireball.net/projects/markdown/">Markdown</a> para formatar o texto.',
            'local': 'Opcional. Você pode usar <a href="http://daringfireball.net/projects/markdown/">Markdown</a> para formatar o texto.',
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


