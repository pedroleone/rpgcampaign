from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from itertools import count
import datetime


class CampaignQuerySet(models.QuerySet):
    def dms(self):
        return self.filter(permission=1)

    def players(self):
        return self.filter(permission=2)

class CampaignManager(models.Manager):
    def get_queryset(self):
        return CampaignQuerySet(self.model, using=self._db)
    
    def dms(self):
        return self.get_queryset().dms()

    def players(self):
        return self.get_queryset().players()

class Campaign(models.Model):
    name = models.CharField(max_length=50)
    system = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    date_created = models.DateField(auto_now_add=True)
    private = models.BooleanField(default=False)
    objects = CampaignManager()
        

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        for x in count(1):
            if not Campaign.objects.filter(slug=slug).exists():
                break
            slug = "%s-%d" % (slug, x)
        
        self.slug = slug
        super(Campaign, self).save(*args, **kwargs)
    


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