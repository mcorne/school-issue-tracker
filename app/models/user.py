from flask import request, url_for
from flask_babel import lazy_gettext as _l
from flask_table import BoolCol, Col, LinkCol, Table

from app.models.common import BaseEnum
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
        if "issue_type" in request.cookies:
            return request.cookies.get("issue_type")

        issue_types = {
            Role.admin.name: None,
            Role.it_manager.name: "computer",
            Role.it_technician.name: "computer",
            Role.service_agent.name: "other",
            Role.service_manager.name: "other",
            Role.teacher.name: None,
        }
        self.validate_role(issue_types)
        return issue_types[self.name]

    def get_urls(self):
        urls = {
            Role.admin.name: [
                {"text": _l("Issues"), "endpoint": "issue.index"},
                {"text": _l("Users"), "endpoint": "user.index"},
            ],
            Role.it_manager.name: [{"text": _l("Issues"), "endpoint": "issue.index"}],
            Role.it_technician.name: [
                {"text": _l("Issues"), "endpoint": "issue.index"}
            ],
            Role.service_agent.name: [
                {"text": _l("Issues"), "endpoint": "issue.index"}
            ],
            Role.service_manager.name: [
                {"text": _l("Issues"), "endpoint": "issue.index"}
            ],
            Role.teacher.name: [{"text": _l("Issues"), "endpoint": "issue.index"}],
        }

        self.validate_role(urls)
        urls = urls[self.name]
        for url in urls:
            if "values" not in url:
                url["values"] = {}
        return urls

    def validate_role(self, urls):
        if self.name not in urls:
            raise ValueError("Unexpected role: {}".format(self.name))


class UserList(Table):
    classes = ["w3-table-all", "w3-hoverable"]
    username = LinkCol(
        _l("Username"),
        "user.update",
        anchor_attrs={"class": "link"},
        attr="username",
        th_html_attrs={"class": "w3-blue w3-hover-gray"},
        url_kwargs=dict(id="id"),
    )  # TODO: escape with flask markup
    role = Col(_l("Role"), th_html_attrs={"class": "w3-blue w3-hover-gray"})
    generic = BoolCol(
        _l("Generic"),
        no_display=_l("No"),
        th_html_attrs={"class": "w3-blue w3-hover-gray"},
        yes_display=_l("Yes"),
    )
    disabled = BoolCol(
        _l("Disabled"),
        no_display=_l("No"),
        th_html_attrs={"class": "w3-blue w3-hover-gray"},
        yes_display=_l("Yes"),
    )

    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        direction = "desc" if reverse else "asc"
        return url_for("user.index", sort=col_key, direction=direction)
