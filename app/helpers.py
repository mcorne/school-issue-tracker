from enum import Enum

from flask import flash, redirect, request, url_for
from flask_babel import _


def fix_row(row, columns):
    fixed = []
    for column in columns:
        value = getattr(row, column) if hasattr(row, column) else None
        fixed.append(fix_value(value))
    return fixed


def fix_rows(rows, headers):
    columns = headers.keys()
    fixed = [fix_row(row, columns) for row in rows]
    fixed.insert(0, headers.values())
    return fixed


def fix_value(value):
    if value == False:
        value = _("No")
    elif value == True:
        value = _("Yes")
    elif isinstance(value, Enum):
        value = value.value

    return value


def get_arg_or_cookie(name):
    if name in request.args:
        return request.args.get(name)
    if name in request.cookies:
        return request.cookies.get(name)


def redirect_unauthorized_action():
    flash(_("You are not authorized to perform this action."), "error")
    return redirect(url_for("user.logout"))
