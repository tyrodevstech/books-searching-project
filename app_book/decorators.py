from functools import wraps
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import Http404


def user_decorator(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.role == "User":
            return function(request, *args, **kwargs)
        else:
            raise Http404

    return wrap


def seller_decorator(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.role == "Shop Owner":
            return function(request, *args, **kwargs)
        else:
            raise Http404

    return wrap
