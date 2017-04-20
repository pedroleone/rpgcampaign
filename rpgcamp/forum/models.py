from django.db import models
from django.contrib.auth.models import User
from campaign.models import Session, Campaign

class Topic(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    title = models.CharField(max_length=250)
    published_date = models.DateTimeField(auto_now_add=True)
    linked_session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,blank=True)
    fixed = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_date"]

class TopicMessage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.text