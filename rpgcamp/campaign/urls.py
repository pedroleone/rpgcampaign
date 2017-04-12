from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new_campaign/$', views.create_campaign, name='create_campaign'),
    url(r'^$', views.index, name='index'),
    
    
]
