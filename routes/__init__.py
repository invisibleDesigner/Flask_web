from functools import wraps
from flask import (
    session,
    abort,
    request,
)
from models.user import User
from models.csrf import Csrf
from utils import log


def current_user():
    # 从 session 中找 user_id 字段, 找不到就返回-1（游客），然后user_id找用户
    user_id = session.get('user_id', -1)
    log('当前session list:{}'.format(session))
    user = User.one(id=user_id)
    return user


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        u = current_user()
        if u is None:
            return abort(401)
        else:
            return f(u, *args, **kwargs)

    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        u = current_user()
        if u is not None and u.is_admin:
            return f(*args, **kwargs)
        else:
            return abort(403)

    return wrapper


def csrf_token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if Csrf.get_csrf() == request.form['csrf_token']:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return wrapper
