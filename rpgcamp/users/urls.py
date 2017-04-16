from django.conf.urls import url
from django.contrib.auth import views as auth_views
from users.views import *

urlpatterns = [
    url(r'^login/', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^password_change/$', auth_views.password_change, {'template_name': 'registration/password_change.html'}, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^new_user/$', add_user, name='add_user'),
    url(r'^profile/$', self_profile, name='self_profile'),
    url(r'^profile/edit/$', edit_profile, name='edit_profile'),
    url(r'^profile/(?P<username>[\w-]+)$', view_profile, name='view_profile'),
]