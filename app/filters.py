import re

import jinja2
from flask import Blueprint
from flask_babel import format_datetime
from jinja2 import Markup, escape

bp = Blueprint("filters", __name__)


def fix_nl(string):
    if string:
        fixed = re.sub("(\r\n|\r)", "\n", string)
        return fixed


@jinja2.contextfilter
@bp.app_template_filter()
def local_datetime(context, datetime):
    return format_datetime(datetime, format="short")


@jinja2.contextfilter
@bp.app_template_filter()
def nl2br(context, string):
    fixed = re.sub(r"(\r\n|\r|\n)", "<br>", escape(string))
    if context.eval_ctx.autoescape:
        fixed = Markup(fixed)
    return fixed
