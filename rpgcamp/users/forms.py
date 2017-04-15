from django.contrib.auth.models import User
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from .models import Profile



class UserForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('display_name', 'profile_pic', 
                  'bio', 'facebook', 'twitter', 'home_city')