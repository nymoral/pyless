from django.contrib.auth import authenticate
import re


def check_len(s, n):
    """Returns true if s is at least n characters long"""
    return s != None and len(s) >= n


def required_missing(form, required):
    """Returns list of names from required that are missing from form"""
    return [name for name in required if form.get(name) is None or len(form.get(name)) == 0]


def too_long_fields(form, fields, n):
    """Returns list of names from fields that exceed length of n"""
    return [name for name in fields if form.get(name) != None and len(form.get(name)) > n]


email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


def is_email(email):
    """Check if given string is a valid email address"""
    return email_pattern.fullmatch(email) != None


def good_password(user, password):
    """Check if given password can authenticate given user"""
    return password != None and authenticate(username=user.username, password=password) != None
