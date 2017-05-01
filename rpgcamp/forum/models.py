from django.db import models
from django.contrib.auth.models import User
from campaign.models import Session, Campaign
from django.utils import timezone
import bleach

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

    def get_pubdate_short(self):
        return timezone.localtime(self.published_date).strftime('%d/%m/%y %H:%M')

    def get_title(self):
        if self.linked_session:
            return 'Tópico da Sessão de ' + self.linked_session.get_date_short()
        else:
            return self.title
    
    def total_messages(self):
        return TopicMessage.objects.filter(topic=self).count()

class TopicMessage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    def get_pubdate_short(self):
        return timezone.localtime(self.published_date).strftime('%d/%m/%y %H:%M')

    def get_moddate_short(self):
        return timezone.localtime(self.modified_date).strftime('%d/%m/%y %H:%M')


    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.text = bleach.clean(self.text)
        super(TopicMessage, self).save(*args, **kwargs)           