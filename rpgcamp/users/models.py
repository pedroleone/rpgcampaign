from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import SmartResize

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = ProcessedImageField(blank=True, upload_to='avatars',
                                           processors=[SmartResize(200, 200)],
                                           format='JPEG',
                                           options={'quality': 65})
    display_name = models.CharField(max_length=50)
    bio = models.CharField(blank=True, max_length=1000)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    home_city = models.CharField(blank=True, max_length=100)
    
    @property
    def get_profile_pic(self):
        if not self.profile_pic:
            return '/static/img/blank_profile_pic.png'
        else:
            return self.profile_pic.url

    def __str__(self):
        return self.display_name