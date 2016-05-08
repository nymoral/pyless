from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout


@require_http_methods(['GET'])    
def logout_view(request):
    """Logout a user and redirect to index page."""
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@require_http_methods(['GET'])    
def index(request):
    """Redirect loged in user to home page or show a login form to others."""
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login'))
