from django.contrib import admin
from forum.models import *

class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'published_date', 'linked_session', 'fixed', 'locked'
    )

class TopicMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'text', 'published_date', 'modified_date'
    )

admin.site.register(Topic,TopicAdmin)
admin.site.register(TopicMessage,TopicMessageAdmin)



