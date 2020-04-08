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
    facility = _l(
        "Facility management request (heating, electricity, broken equipment, cleanliness etc.)"
    )
    it = _l("IT support request (computer, printer, cartridge, network etc.)")

    def is_it(self):
        return self == Type.it
