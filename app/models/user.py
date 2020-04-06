from flask_babel import lazy_gettext as _l

from app.helpers import get_arg_or_cookie
from app.models.common import BaseEnum, MyLinkCol, MyTable
from app.models.issue import Type


class Role(BaseEnum):
    admin = _l("Administrator")
    it_manager = _l("IT Manager")
    it_technician = _l("IT Technician")
    service_agent = _l("Service Agent")
    service_manager = _l("Service Manager")
    teacher = _l("Teacher")

    def authorized(self, action, issue):
        authorizations = {
            "change_to_computer_issue": lambda role, issue: not issue.is_closed()
            and issue.type == Type.other
            and role in (Role.admin, Role.service_manager, Role.service_agent),
            ##
            "change_to_technical_issue": lambda role, issue: not issue.is_closed()
            and issue.type == Type.computer
            and role in (Role.admin, Role.it_manager, Role.it_technician),
            ##
            "close_issue": lambda role, issue: not issue.is_closed()
            and (
                issue.type == Type.computer
                and role in (Role.admin, Role.it_manager)
                or issue.type == Type.other
                and role in (Role.admin, Role.service_manager)
            ),
            ##
            "reopen_issue": lambda role, issue: issue.is_closed(),
            ##
            "update_issue": lambda role, issue: not issue.is_closed()
            and (
                issue.type == Type.computer
                and role in (Role.admin, Role.it_manager, Role.it_technician)
                or issue.type == Type.other
                and role in (Role.admin, Role.service_manager, Role.service_agent)
            ),
        }

        if action not in authorizations:
            raise ValueError("Unexpected action: {}".format(action))

        return authorizations[action](self, issue)

    def get_default_url(self):
        urls = {
            Role.admin.name: "issue.index",
            Role.it_manager.name: "issue.index",
            Role.it_technician.name: "issue.index",
            Role.service_agent.name: "issue.index",
            Role.service_manager.name: "issue.index",
            Role.teacher.name: "issue.create",
        }
        self.validate_role(urls)
        return urls[self.name]

    def get_issue_type(self):
        issue_type = get_arg_or_cookie("issue_type")
        if issue_type in ("all", Type.computer.name, Type.other.name):
            return issue_type

        issue_types = {
            Role.admin.name: "all",
            Role.it_manager.name: Type.computer.name,
            Role.it_technician.name: Type.computer.name,
            Role.service_agent.name: Type.other.name,
            Role.service_manager.name: Type.other.name,
            Role.teacher.name: "all",
        }
        self.validate_role(issue_types)
        return issue_types[self.name]

    def validate_role(self, urls):
        if self.name not in urls:
            raise ValueError("Unexpected role: {}".format(self.name))


class UserLinkCol(MyLinkCol):
    endpoint = "user.update"


class UserTable(MyTable):
    endpoint = "user.index"
    username = UserLinkCol(_l("Username"), "username")
    role = UserLinkCol(_l("Role"), "role")
    generic = UserLinkCol(_l("Generic"), "generic")
    disabled = UserLinkCol(_l("Disabled"), "disabled")
