from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods

from football.models import Reminder

@require_http_methods(['GET', 'POST'])
def reset_view(request, reminderId):
    r = Reminder.objects.filter(id=reminderId).select_related('user')
    if len(r) == 0:
        return HttpResponseRedirect(request.POST.get('next_url', reverse('index')))
    r = r[0]
    ctx = {'reminderId': str(r.id), 'username': r.user.username}
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat = request.POST.get('repeat', '')
        if len(password) < 6 or password != repeat:
            ctx['error'] = True
        else:
            u = r.user
            u.set_password(password)
            u.save()
            ctx['success'] = True
            r.delete()
        

    return render(request, 'football/reset.html', ctx)
