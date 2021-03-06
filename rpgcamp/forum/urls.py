from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^c/(?P<slug>[\w-]+)/forum/$', views.view_forum, name='view_forum'),
    url(r'^c/(?P<slug>[\w-]+)/forum/new_topic/$', views.new_topic, name='new_topic'),
    url(r'^c/(?P<slug>[\w-]+)/forum/new_topic/(?P<session_id>[\w-]+)/$', views.new_topic_from_session, name='new_topic_from_session'),
    url(r'^c/(?P<slug>[\w-]+)/forum/topic/(?P<topic_id>[\w-]+)/$', views.view_topic, name='view_topic'),
    url(r'^c/(?P<slug>[\w-]+)/forum/topic/(?P<topic_id>[\w-]+)/edit/$', views.edit_topic, name='edit_topic'),
    url(r'^c/(?P<slug>[\w-]+)/forum/topic/(?P<topic_id>[\w-]+)/edit/(?P<message_id>[\w-]+)$', views.edit_message, name='edit_message'),
]


