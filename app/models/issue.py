from enum import Enum

from flask_babel import lazy_gettext as _l
from flask_table import BoolCol, Col, LinkCol, Table


class Site(Enum):  # TODO: refactor with Role etc.
    marie_curie = "Marie-Curie"
    molière = "Molière"

    def __html__(self):
        return self.value

    def __str__(self):
        return self.name

    @classmethod
    def coerce(cls, value):
        if isinstance(value, Site):
            value = value.name
        return value

    @classmethod
    def get_choices(cls):
        choices = [(site.name, site.value) for site in cls.__members__.values()]
        return choices


class Type(Enum):  # TODO: refactor with Role etc.
    computer = _l("Computer related issue or request")
    other = _l(
        "Technical issue (heating, electricity, broken equipment, cleanliness etc.)"
    )

    def __html__(self):
        return self.value

    def __str__(self):
        return self.name

    @classmethod
    def coerce(cls, value):
        if isinstance(value, Type):
            value = value.name
        return value

    @classmethod
    def get_choices(cls):
        choices = [(type.name, type.value) for type in cls.__members__.values()]
        return choices
