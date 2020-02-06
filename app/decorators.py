from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if current_user.role.name not in roles:
                flash("You are not authorized to perform this action.")
                return redirect(url_for("user.login"))

            return f(*args, **kwargs)

        return decorator

    return wrapper
