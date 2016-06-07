from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.conf import settings


@require_http_methods(['GET', 'POST'])
def login_view(request, username=None):
    """Login page view
    It renders empty login form on GET and tries to authenticate a user on POST.
    """

    if request.method == 'GET':
        ctx = {'username': username} if username else {}
        ctx['next_url'] = request.GET.get('next', reverse('index'))
        return render_login(request, ctx)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember') != None
        return do_login(request, username, password, remember)


def render_login(request, ctx=None):
    """Helper renderer that add 'REGISTER_ENABLED' variable to templates context"""
    if ctx is None:
        ctx = {}
    ctx['register_enabled'] = settings.REGISTER_ENABLED
    return render(request, 'football/login.html', ctx)


def do_login(request, username, password, remember):
    """Perform the login routine.
    If authentication is successful, user is redirected to root (index) page.
    Otherwise, login form with errors and entered username / remember fields is rendered.
    """
    next_url = request.POST.get('next_url', reverse('index'))
    ctx = {'username': username, 'remember': remember, 'next_url': next_url}

    def redraw():
        return render_login(request, ctx)

    if username is None or password is None:
        ctx['required_error'] = True
        return redraw()

    user = authenticate(username=username.lower(), password=password)
    if user is None:
        ctx['auth_error'] = True
        return redraw()

    if not user.is_active:
        ctx['active_error'] = True
        return redraw()
    if not remember:
        request.session.set_expiry(0)
    login(request, user)
    return HttpResponseRedirect(next_url)
