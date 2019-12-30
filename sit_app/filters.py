import jinja2
from flask import Blueprint
from flask_babel import format_datetime

bp = Blueprint('filters', __name__)


# using the decorator
@jinja2.contextfilter
@bp.app_template_filter()
def local_datetime(context, datetime):
    return format_datetime(datetime, format='short')
