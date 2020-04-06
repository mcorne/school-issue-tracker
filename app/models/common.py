from enum import Enum

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
    def __init__(self, name, endpoint, attr, **kwargs):
        super().__init__(
            attr=attr,
            endpoint=endpoint,
            name=name,
            th_html_attrs={"class": "w3-blue w3-hover-gray"},
            url_kwargs=dict(id="id"),
            **kwargs
        )
