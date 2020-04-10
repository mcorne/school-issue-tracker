from flask_babel import lazy_gettext as _l

from app.helpers import get_arg_or_cookie
from app.models.common import BaseEnum, MyLinkCol, MyTable
from app.models.issue import Type


class Role(BaseEnum):
    admin = _l("Administrator")
    facility_support_1 = _l("Facility management support L1")
    facility_support_2 = _l("Facility management support L2")
    it_support_1 = _l("IT support L1")
    it_support_2 = _l("IT support L2")
    teacher = _l("Teacher")

    def authorized(self, action, issue=None):
        authorizations = {
            "change_to_facility_issue": lambda role, issue: not issue.is_closed()
            and issue.type == Type.it
            and role in (Role.admin, Role.it_support_2, Role.it_support_1),
            ##
            "change_to_it_issue": lambda role, issue: not issue.is_closed()
            and issue.type == Type.facility
            and role in (Role.admin, Role.facility_support_2, Role.facility_support_1),
            ##
            "close_issue": lambda role, issue: not issue.is_closed()
            and (
                issue.type == Type.it
                and role in (Role.admin, Role.it_support_2)
                or issue.type == Type.facility
                and role in (Role.admin, Role.facility_support_2)
            ),
            ##
            "download_issue": lambda role, issue: role
            in (Role.admin, Role.it_support_2, Role.facility_support_2),
            ##
            "reopen_issue": lambda role, issue: issue.is_closed(),
            ##
            "update_issue": lambda role, issue: not issue.is_closed()
            and (
                issue.type == Type.it
                and role in (Role.admin, Role.it_support_2, Role.it_support_1)
                or issue.type == Type.facility
                and role
                in (Role.admin, Role.facility_support_2, Role.facility_support_1)
            ),
        }

        if action not in authorizations:
            raise ValueError("Unexpected action: {}".format(action))

        return authorizations[action](self, issue)

    def get_default_url(self):
        urls = {
            Role.admin.name: "issue.index",
            Role.it_support_2.name: "issue.index",
            Role.it_support_1.name: "issue.index",
            Role.facility_support_1.name: "issue.index",
            Role.facility_support_2.name: "issue.index",
            Role.teacher.name: "issue.create",
        }
        self.validate_role(urls)
        return urls[self.name]

    def get_issue_type(self):
        issue_type = get_arg_or_cookie("issue_type")
        if issue_type in ("all", Type.it.name, Type.facility.name):
            return issue_type

        issue_types = {
            Role.admin.name: "all",
            Role.it_support_2.name: Type.it.name,
            Role.it_support_1.name: Type.it.name,
            Role.facility_support_1.name: Type.facility.name,
            Role.facility_support_2.name: Type.facility.name,
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
