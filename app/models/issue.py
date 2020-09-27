from app.models.common import BaseEnum
from flask import current_app
from flask_babel import lazy_gettext as _l


class SiteZZZ(BaseEnum): # TODO: make generic and define key/value in config, use site 1, 2 etc.
    marie_curie = "Marie Curie"
    molière = "Molière" # TODO: remove accent in key in code and database including constraints

if "SITES" in current_app.config: # TODO: fix !!!
    raise ValueError("SITES missing in config.py")
Site = BaseEnum("Site", current_app.config["SITES"], module=__name__)

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
    # Do not change the order for displaying purposes in the issue creation form
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
