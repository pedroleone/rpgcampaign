from django.contrib.auth.models import User
from django.forms import ModelForm
from captcha.fields import ReCaptchaField


class UserForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password')