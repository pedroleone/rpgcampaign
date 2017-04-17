from django.contrib import admin
from campaign.models import Campaign, CampaignUser, Session

class CampaignAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Campaign,CampaignAdmin)
admin.site.register(CampaignUser)
admin.site.register(Session)