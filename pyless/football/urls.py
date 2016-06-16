from django.conf.urls import url, include

from .views.helpers import logout_view, index, rules_view
from .views.home import home
from .views.login import login_view
from .views.register import register_view
from .views.user_edit import settings_view
from .views.guesses import guesses_view, guess_ajax
from .views.results import results_view, results_small_view 
from .views.game import game_view
from .views.forgot import forgot_view
from .views.reset import reset_view

urlpatterns = [
    url(r'^auth/logout/$', logout_view, name='logout'),
    url(r'^auth/login/$', login_view, name='login'),
    url(r'^auth/login/(?P<username>.+)/$', login_view, name='login_username'),
    url(r'^auth/register/$', register_view, name='register'),
    url(r'^auth/settings/$', settings_view, name='settings'),
    url(r'^auth/forgot/$', forgot_view, name='forgot'),
    url(r'^auth/reset/(?P<reminderId>.+)/$', reset_view, name='reset_view'),
    url(r'^home/$', home, name='home'),
    url(r'^guesses/(?P<user_id>\d+)/$', guesses_view, name='guesses'),
    url(r'^guesses/(?P<user_id>\d+)/(?P<game_id>\d+)/(?P<g1>\d+)/(?P<g2>\d+)/$', guess_ajax, name='guess_ajax'),
    url(r'^results/full/$', results_view, name='results_full'),
    url(r'^results/$', results_small_view, name='results'),
    url(r'^game/(?P<game_id>\d+)/$', game_view, name='game_view'),
    url(r'^rules/$', rules_view, name='rules'),
    url(r'^$', index, name='index'),
]
