from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    """
    Decorator to restrict route access to 'admin' users only.
    Throws a 403 Forbidden error if unauthorized.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def member_required(f):
    """
    Decorator to restrict route access to 'member' users only.
    Throws a 403 Forbidden error if unauthorized.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'member':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
