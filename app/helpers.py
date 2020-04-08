from urllib.parse import urljoin, urlparse

from flask import flash, redirect, request, url_for
from flask_babel import _


def get_arg_or_cookie(name):
    if name in request.args:
        return request.args.get(name)
    if name in request.cookies:
        return request.cookies.get(name)


def redirect_unauthorized_action():
    flash(_("You are not authorized to perform this action."), "error")
    return redirect(url_for("user.logout"))
