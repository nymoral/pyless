from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required()
@require_http_methods(['GET'])
def home(request):
    return render(request, 'football/home.html')
