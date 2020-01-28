from flask import url_for
from flask_babel import lazy_gettext as _l
from flask_table import BoolCol, Col, LinkCol, Table

from app.models.common import BaseEnum


class Role(BaseEnum):
    admin = _l("Administrator")
    teacher = _l("Teacher")
    it_technician = _l("IT Technician")
    it_manager = _l("IT Manager")
    service_agent = _l("Service Agent")
    service_manager = _l("Service Manager")

    def get_default_url(self):
        urls = {
            "admin": {"endpoint": "issue.index"},
            "teacher": {"endpoint": "issue.create"},
            "it_technician": {"endpoint": "issue.index", "type": "computer"},
            "it_manager": {"endpoint": "issue.index", "type": "computer"},
            "service_agent": {"endpoint": "issue.index", "type": "other"},
            "service_manager": {"endpoint": "issue.index", "type": "other"},
        }
        if self.name not in urls:
            raise ValueError("Unexpected role: {}".format(self.name))
        return urls[self.name]


class UserList(Table):
    username = LinkCol(
        _l("Username"), "user.update", url_kwargs=dict(id="id"), attr="username"
    )  # TODO: escape with flask markup
    role = Col(_l("Role"))
    generic = BoolCol(_l("Generic"), yes_display=_l("Yes"), no_display=_l("No"))
    disabled = BoolCol(_l("Disabled"), yes_display=_l("Yes"), no_display=_l("No"))

    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        direction = "desc" if reverse else "asc"
        return url_for("user.index", sort=col_key, direction=direction)
