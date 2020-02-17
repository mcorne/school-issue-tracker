from flask_babel import lazy_gettext as _l

from app.models.common import BaseEnum


class IssueType(BaseEnum):
    computer = _l("Computer related issue or request")
    other = _l(
        "Technical issue (heating, electricity, broken equipment, cleanliness etc.)"
    )


class Site(BaseEnum):
    marie_curie = "Marie-Curie"
    molière = "Molière"
