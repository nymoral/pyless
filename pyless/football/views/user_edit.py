from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .register import validate
from .validation import good_password


@login_required()
@require_http_methods(['GET', 'POST'])
def settings_view(request):
    """Update page view.
    On GET form with models data is displayed.
    On POST either the model is updated, or form with error messages and entered values is displayed.
    If update succeeds, form with new values is displayed"""

    ctx = {'is_edit': True}
    if request.method == 'POST':
        do_update(request, ctx)
    else:
        ctx['data'] = data_from_user(request.user)

    return render(request, 'football/user.html', ctx)


def data_from_user(user):
    """Return templates context with values from user model"""
    data = {}
    data['username'] = user.username
    data['email'] = user.email
    data['firstname'] = user.first_name
    data['lastname'] = user.last_name
    return data


def do_update(request, ctx):
    """Perform validation and update user object"""
    form = request.POST

    change_pass = len(form.get('password', '')) > 0

    if not validate(form, ctx, change_pass):
        return

    if change_pass and not good_password(request.user, form.get('current_password')):
        ctx['current_password_error'] = True
        return

    u = request.user
    u.username = form.get('username').lower()
    u.first_name = form.get('firstname')
    u.last_name = form.get('lastname')
    u.email = form.get('email')
    if change_pass:
        u.set_password(form.get('password'))

    ctx['data'] = data_from_user(u)

    try:
        u.save()
    except IntegrityError:
        ctx['exists_error'] = True
    else:
        ctx['edit_success'] = True
        update_session_auth_hash(request, u)
