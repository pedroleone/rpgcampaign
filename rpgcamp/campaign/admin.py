from django.contrib import admin
from campaign.models import *

class CampaignAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Campaign,CampaignAdmin)
admin.site.register(CampaignUser)
admin.site.register(Session)
admin.site.register(SessionUser)