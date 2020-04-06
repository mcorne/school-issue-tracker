from enum import Enum

from flask import request, url_for
from flask_babel import lazy_gettext as _l
from flask_table import LinkCol, Table


class BaseEnum(Enum):
    def __html__(self):
        return self.value

    def __str__(self):
        return self.name

    @classmethod
    def coerce(cls, value):
        if isinstance(value, cls):
            value = value.name
        return value

    @classmethod
    def get_options(cls, blank_option=None):
        options = []
        if blank_option:
            options += [("", blank_option)]
        options += [(option.name, option.value) for option in cls.__members__.values()]
        return options


class MyLinkCol(LinkCol):
    endpoint = None

    def __init__(self, name, attr, **kwargs):
        super().__init__(
            attr=attr,
            endpoint=self.endpoint,
            name=name,
            th_html_attrs={"class": "w3-blue w3-hover-gray"},
            url_kwargs=dict(id="id"),
            **kwargs
        )

    def td_format(self, content):
        if content == False:
            content = _l("No")
        elif content == True:
            content = _l("Yes")
        elif hasattr(content, "__html__") and callable(content.__html__):
            content = content.__html__()
        return super().td_format(content)


class MyTable(Table):
    allow_sort = True
    classes = ["w3-table-all", "w3-hoverable"]
    endpoint = None
    no_items = ""

    def get_tr_attrs(self, item):
        id = request.args.get("id")
        tr_attrs = {}
        if id and item.id == int(id):
            tr_attrs["class"] = "w3-pale-green"
        return tr_attrs

    def sort_url(self, col_key, reverse=False):
        direction = "desc" if reverse else "asc"
        return url_for(self.endpoint, sort=col_key, direction=direction)
