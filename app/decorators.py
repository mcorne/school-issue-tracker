from functools import wraps

from flask_login import current_user

from app.helpers import redirect_unauthorized_action


def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if current_user.role not in roles:
                return redirect_unauthorized_action()
            return f(*args, **kwargs)

        return decorator

    return wrapper
