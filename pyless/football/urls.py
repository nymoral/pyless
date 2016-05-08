from django.conf.urls import url, include

from .views.helpers import logout_view, index
from .views.home import home
from .views.login import login_view
from .views.register import register_view
from .views.user_edit import settings_view


urlpatterns = [
    url(r'^auth/logout/$', logout_view, name='logout'),
    url(r'^auth/login/$', login_view, name='login'),
    url(r'^auth/login/(?P<username>.+)/$', login_view, name='login-username'),
    url(r'^auth/register/$', register_view, name='register'),
    url(r'^auth/settings/$', settings_view, name='settings'),
    url(r'^home/$', home, name='home'),
    url(r'^$', index, name='index')
]
