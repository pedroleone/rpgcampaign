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
        dm_list = []
        dm_obj = CampaignUser.objects.filter(campaign=self, permission=1)
        for dm in dm_obj:
            dm_list.append(dm.user.profile.display_name)
        return dm_list

    def players(self):
        players_list = []
        players = CampaignUser.objects.filter(campaign=self, permission=2)
        for player in players:
            players_list.append(player.user.profile.display_name)
        return players_list

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