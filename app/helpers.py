from urllib.parse import urljoin, urlparse

from flask import flash, redirect, request, url_for
from flask_babel import _


def get_arg_or_cookie(name):
    if name in request.args:
        return request.args.get(name)
    if name in request.cookies:
        return request.cookies.get(name)


# see https://github.com/fengsp/flask-snippets/blob/master/security/redirect_back.py
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def redirect_unauthorized_action():
    flash(_("You are not authorized to perform this action."), "error")
    return redirect(url_for("user.logout"))
