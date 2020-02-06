from functools import wraps

from flask import current_app, flash, redirect, request, url_for
from flask_login import current_user

from app.models.user import Role


def authorize_action(f):
    def authorization_error():
        flash("You are not authorized to perform this action.")
        return redirect(url_for("user.login"))

    @wraps(f)
    def wrapper(*args, **kwargs):
        actions = {
            "change_type": ("admin", "it_manager", "service_manager"),
        }
        if f.__name__ not in actions:
            raise ValueError("Invalid action: {}".format(f.__name__))
        if current_user.role.name not in actions[f.__name__]:
            authorization_error()
        if f.__name__ in (
            "create_issue",
            "update_issue",
        ):  # TODO: fix create_issue vs create + bp !!!
            issue_type = request.args.get("type")
            if issue_type == "computer":
                if current_user.role.name not in (
                    "admin",
                    "it_manager",
                    "it_technician",
                ):
                    pass
        return f(*args, **kwargs)

    return wrapper

