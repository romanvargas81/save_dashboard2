"""Module containing decorators."""

from flask import request, abort, current_app
from functools import wraps
from warnings import warn

from .utils import _get_user, current_user


def __add_user_to_request(request):
    if hasattr(request, 'user'):
        return

    setattr(request, 'user', _get_user())



def role_restriction(service, level):
    """Check the role permission to access a view."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.check(service, level):
                abort(403)

            return func(*args, **kwargs)
        return wrapper
    return decorator


def role_based(func):
    """Set the roles if they are present on the request."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        __add_user_to_request(request)
        warn("@role_based is deprecated, please use current_user import instead", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper
