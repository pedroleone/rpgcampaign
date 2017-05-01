from django.contrib import admin
from campaign.models import *

class CampaignAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = (
        'name', 'system', 'description','slug','date_created','private'
    )

class CampaignUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'campaign', 'permission', 'user_email'
    )

    def user_email(self, obj):
        return obj.user.email

class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'campaign', 'date', 'notes', 'local'
    )
    
class SessionUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'campaign', 'session', 'status', 'note'
    )

class HouseRulesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'campaign', 'text', 'gm_only_text', 'published_date', 'modified_date'
    )

class GameReportAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'linked_session', 'published_date', 'modified_date', 'text', 'gm_only_text','author', 'campaign'
    )
    

admin.site.register(Campaign,CampaignAdmin)
admin.site.register(CampaignUser, CampaignUserAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(SessionUser, SessionUserAdmin)
admin.site.register(HouseRules, HouseRulesAdmin)
admin.site.register(GameReport, GameReportAdmin)
