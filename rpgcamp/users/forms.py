from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from .models import Profile
from django import forms


class UserForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('display_name', 'profile_pic', 
                  'bio', 'facebook', 'twitter', 'home_city')


class UserProfileNewForm(forms.Form):
    username = forms.CharField(label='Nome de Usuário', max_length=150, help_text="Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas. Você não vai poder alterá-lo depois")
    email = forms.EmailField(label='E-mail',help_text='Obrigatório. Utilize um e-mail válido')
    display_name = forms.CharField(label='Nome de Exibição',max_length=50,help_text="O nome que irá ser exibido para seu usuário dentro das campanhas. Você pode alterá-lo depois.")
    home_city = forms.CharField(required=False,label='Cidade',max_length=100,help_text="Não obrigatório")
    bio = forms.CharField(required=False,label='Informações Pessoais',max_length=1000,help_text="Não obrigatório. Qualquer informação que você quer deixar pública no sistema: quais sistemas você joga, se prefere mestrar a jogar, etc.")
    facebook = forms.URLField(label='Facebook',required=False,help_text='Não obrigatório')
    twitter = forms.URLField(label='Twitter',required=False,help_text='Não obrigatório')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Confirme sua Senha', widget=forms.PasswordInput)
    captcha = ReCaptchaField()

    def clean(self):
        cleaned_data = super(UserProfileNewForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            msg = 'Senha e Confirmação da senha não estão iguais. Confirme a digitação.'
            self.add_error('password_confirmation', msg)
            