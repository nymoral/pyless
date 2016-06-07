from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .validation import is_email
from football.models import Reminder

from threading import Thread

@require_http_methods(['GET', 'POST'])
def forgot_view(request):
    if request.method == 'GET':
        return render(request, 'football/forgot.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username', '')
        ctx = {'email': email, 'username': username}
        if not is_email(email) or len(username) == 0:
            ctx['error'] = True
        else:
            ctx['success'] = True
            do_send(request, email, username)
        return render(request, 'football/forgot.html', ctx)


def do_send(request, email, username):
    u = User.objects.filter(email=email, username=username.lower())
    if len(u) == 0:
        return
    r = Reminder(user=u[0])
    r.save()
    link = request.build_absolute_uri(reverse('reset_view', kwargs={'reminderId': r.id}))

    send_reminder(email, link)

def mailer(email, link):
    def target():
        send_mail('Totalizatorius: slaptažodžio atkūrimas', link, 'totalizatorius@aivaras.me',
        [email])
        print('Email to {} sent'.format(email))
    return target

def send_reminder(email, link):
    t = Thread(target=mailer(email, link))
    t.start()