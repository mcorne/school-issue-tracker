from flask_babel import lazy_gettext as _l

from app.models.common import BaseEnum


class Site(BaseEnum):
    marie_curie = "Marie Curie"
    molière = "Molière"


class Status(BaseEnum):
    pending = 1
    processing = 2
    closed = 3


class Type(BaseEnum):
    computer = _l("IT support request (computer, printer, network etc.")
    facility = _l(
        "Facility management request (heating, electricity, broken equipment, cleanliness etc.)"
    )

    def is_computer(self):
        return self == Type.computer
