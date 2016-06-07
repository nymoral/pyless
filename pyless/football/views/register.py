from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError

from .validation import check_len, required_missing, too_long_fields, is_email


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if not settings.REGISTER_ENABLED:
        return HttpResponseForbidden()
    if request.method == 'GET':
        return render(request, 'football/user.html')
    else:
        return do_register(request)

required__no_pass = ('username', 'firstname', 'lastname', )
required_fields = required__no_pass + ('password', 'repeat', )


def extract_data(data):
    user = {}
    user['username'] = data.get('username').lower()
    user['first_name'] = data.get('firstname')
    user['last_name'] = data.get('lastname')
    user['email'] = data.get('email')
    return user


def validate(form, ctx, check_pass=True):
    n_errors = 0

    def add_error(name, value=True):
        ctx[name] = value
        nonlocal n_errors
        n_errors += 1

    # Perform required fields validation
    required = required_missing(form, required_fields if check_pass else required__no_pass)
    if len(required) > 0:
        add_error('required_error')
        add_error('required', {name: True for name in required})

    # Check if no field is longer than 30 chars
    if len(too_long_fields(form, ('firstname', 'lastname'), 30)) > 0:
        add_error('input_length_error')

    if check_pass:
        password = form.get('password')
        # Check for password length
        if  not check_len(password, 6):
            add_error('password_req_error')

        # Check if passwords match
        if password != form.get('repeat'):
            add_error('password_match_error')

    email = form.get('email')
    # If email was entered check if its format is good.
    if check_len(email, 1) and not is_email(email):
        add_error('email_format_error')

    return n_errors == 0


def do_register(request):
    data = request.POST
    ctx = {'data': data}

    def redraw():
        return render(request, 'football/user.html', ctx)

    if validate(data, ctx):
        u = User(**extract_data(data))
        u.set_password(data.get('password'))
        try:
            u.save()
        except IntegrityError:
            ctx['exists_error'] = True
        else:
            ctx['success'] = True
    return redraw()
