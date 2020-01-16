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


class UserList(Table):
    id = LinkCol(
        _l("Username"),
        "user.update",
        attr="username",
        url_kwargs=dict(id="id"),  # TODO: escape with flask markup
    )
    role = Col(_l("Role"))
    generic = BoolCol(_l("Generic"), yes_display=_l("Yes"), no_display=_l("No"))
    disabled = BoolCol(_l("Disabled"), yes_display=_l("Yes"), no_display=_l("No"))
