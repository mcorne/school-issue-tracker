import jinja2
from babel.dates import format_datetime, get_timezone
from flask import Blueprint

bp = Blueprint('filters', __name__)


# using the decorator
@jinja2.contextfilter
@bp.app_template_filter()
def local_datetime(context, datetime):
    timezone = get_timezone('Europe/Vienna')  # TODO: set timezone in config
    return format_datetime(datetime,
                           format='short',
                           tzinfo=timezone,
                           locale='fr')  # TODO: set local in config
