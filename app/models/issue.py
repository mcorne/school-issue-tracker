from flask_babel import lazy_gettext as _l

from app.models.common import BaseEnum


class Site(BaseEnum):
    marie_curie = "Marie Curie"
    molière = "Molière"


class Status(BaseEnum):
    pending = 1
    processing = 2
    closed = 3

    def get_short_values(self):
        return {
            "pending": _l("Pending"),
            "processing": _l("Processing"),
            "closed": _l("Closed"),
        }


class Type(BaseEnum):
    # do not change the order for displaying purposes
    it = _l("IT support request (computer, printer, cartridge, network etc.)")
    facility = _l(
        "Facility management request (heating, electricity, broken equipment, cleanliness etc.)"
    )

    def get_short_values(self):
        return {
            "it": _l("IT"),
            "facility": _l("Facility management"),
        }

    def is_it(self):
        return self == Type.it
