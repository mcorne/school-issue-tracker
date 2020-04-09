from datetime import datetime
from enum import Enum

from flask import flash, redirect, request, url_for
from flask_babel import _, format_datetime


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
    if value == None:
        value = ""
    elif value == False:
        value = _("No")
    elif value == True:
        value = _("Yes")
    elif isinstance(value, Enum):
        short_values = value.get_short_values()
        if value.name in short_values:
            value = short_values[value.name]
        else:
            value = value.value
        value = str(value)  # must cast translations to string
    elif isinstance(value, datetime):
        value = format_datetime(value, format="short")
    return value


def get_arg_or_cookie(name):
    if name in request.args:
        return request.args.get(name)
    if name in request.cookies:
        return request.cookies.get(name)


def redirect_unauthorized_action():
    flash(_("You are not authorized to perform this action."), "error")
    return redirect(url_for("user.logout"))
