from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new_campaign/$', views.create_campaign, name='create_campaign'),
    url(r'^c/(?P<slug>[\w-]+)/$', views.view_campaign, name='view_campaign'),
    url(r'^c/(?P<slug>[\w-]+)/newsession/$', views.new_session, name='new_session'),
    url(r'^c/(?P<slug>[\w-]+)/sessions/$', views.view_sessions, name='view_sessions'),
    url(r'^c/(?P<slug>[\w-]+)/sessions/(?P<session_id>[\w-]+)$', views.view_session, name='view_session'),
    url(r'^c/(?P<slug>[\w-]+)/sessions/(?P<session_id>[\w-]+)/edit$', views.edit_session, name='edit_session'),
    url(r'^c/(?P<slug>[\w-]+)/players/$', views.players, name='players'),
    url(r'^c/(?P<slug>[\w-]+)/players/delete/$', views.delete_player, name='delete_player'),
    url(r'^$', views.index, name='index'),
]
