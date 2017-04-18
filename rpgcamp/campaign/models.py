from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from itertools import count
import datetime


class Campaign(models.Model):
    name = models.CharField(max_length=50)
    system = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    date_created = models.DateField(auto_now_add=True)
    private = models.BooleanField(default=False)
        

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        for x in count(1):
            if not Campaign.objects.filter(slug=slug).exists():
                break
            slug = "%s-%d" % (slug, x)
        
        self.slug = slug
        super(Campaign, self).save(*args, **kwargs)
    
    def dms(self):
        participant_list = []
        participants = CampaignUser.objects.filter(campaign=self, permission=1)
        for p in participants:
            participant_list.append({'display_name': p.user.profile.display_name, 
                            'username': p.user.username,
                            'profile_pic': p.user.profile.get_profile_pic,
                            'id': p.user.id})
        return participant_list

    def players(self):
        participant_list = []
        participants = CampaignUser.objects.filter(campaign=self, permission=2)
        for p in participants:
            participant_list.append({'display_name': p.user.profile.display_name, 
                            'username': p.user.username,
                            'profile_pic': p.user.profile.get_profile_pic,
                            'id': p.user.id})
        return participant_list

    def __str__(self):
        return self.name

class CampaignUser(models.Model):
    USER_TYPE = ( (1,'Game Master'), 
                  (2, 'Player') )

    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    permission = models.IntegerField(choices=USER_TYPE, default=2)

    def __str__(self):
        return self.campaign.name


class CampaignNotes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    gm_only = models.BooleanField(default=True)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=False)


class Session(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date = models.DateTimeField()    
    notes = models.TextField(blank=True)
    local = models.TextField(blank=True)

    class Meta:
        ordering = ["date"]

    def save(self, *args, **kwargs):
        super(Session, self).save(*args, **kwargs)
        player_list = CampaignUser.objects.filter(campaign=self.campaign)
        session_user = SessionUser.objects.filter(campaign=self.campaign, 
                                                  session=self)
        if session_user:
            session_user.delete()
        
        for player in player_list:
            session_user = SessionUser(campaign=self.campaign, 
                                       session=self,
                                       user=player.user)
            session_user.save()




class SessionUser(models.Model):
    OPTIONS = (   (1,'Não Informado'), 
                  (2,'Não Vai Participar'), 
                  (3, 'Vai Participar') ,
                  (4, 'Não Sabe')
              )

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.IntegerField(choices=OPTIONS, default=1)
    note = models.CharField(max_length=100)