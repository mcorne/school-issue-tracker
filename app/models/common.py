from enum import Enum

from flask_babel import lazy_gettext as _l


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
