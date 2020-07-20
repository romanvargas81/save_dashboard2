from werkzeug.local import LocalProxy
from flask import (
    _request_ctx_stack, has_request_context, request, current_app
)
from .jwt import decode_token
from .user import User

current_user = LocalProxy(lambda: _get_user())


def __load_user():
    token = request.headers.get('x-hcx-auth-jwt-assertion', False)

    if not token:
        return User(authenticated=False)

    should_verify = current_app.config.get('HCG_UTILS_AUTHENTICATION_JWT_VERIFY', True)
    data = decode_token(token, verify=should_verify)

    if not data:
        return User(authenticated=False)

    user_data = data.get('com.hcgfunds.hcx/user')
    if not user_data:
        return User(authenticated=False)

    user_roles = user_data.get('roles')
    user_identifier = user_data.get('identifier')
    roles = {(r[0], r[1]) for r in user_roles}
    user = User(authenticated=True, roles=roles, identifier=user_identifier)
    user.first_name = user_data.get('first_name')
    user.last_name = user_data.get('last_name')

    return user


def _get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        _request_ctx_stack.top.user = __load_user()
    return getattr(_request_ctx_stack.top, 'user', None)
