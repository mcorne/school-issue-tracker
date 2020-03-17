from flask_babel import lazy_gettext as _l

from app.models.common import BaseEnum


class Site(BaseEnum):
    marie_curie = "Marie Curie"
    molière = "Molière"


class Type(BaseEnum):
    computer = _l("Computer related issue")
    other = _l(
        "Technical issue (heating, electricity, broken equipment, cleanliness etc.)"
    )
