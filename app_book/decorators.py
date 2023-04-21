from functools import wraps
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import Http404


def custom_dec(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        print(request.user)
        if not request.user.is_superuser:
            print("Yes")
            return function(request, *args, **kwargs)
        else:
            print('No')
            raise Http404
    return wrap
