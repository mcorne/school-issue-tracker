from flask import request, url_for
from flask_babel import lazy_gettext as _l
from flask_table import BoolCol, Col, LinkCol, Table

from app.models.common import BaseEnum


class Role(BaseEnum):
    admin = _l("Administrator")
    it_manager = _l("IT Manager")
    it_technician = _l("IT Technician")
    service_agent = _l("Service Agent")
    service_manager = _l("Service Manager")
    teacher = _l("Teacher")

    def authorized(self, action, **kwargs):
        authorizations = {
            "change_to_computer_issue": lambda role, issue: not issue.closed
            and issue.type.name == "other"
            and role in ("admin", "service_manager", "service_agent"),
            ##
            "change_to_technical_issue": lambda role, issue: not issue.closed
            and issue.type.name == "computer"
            and role in ("admin", "it_manager", "it_technician"),
            ##
            "close_issue": lambda role, issue: not issue.closed
            and (
                issue.type.name == "computer"
                and role in ("admin", "it_manager")
                or issue.type.name == "other"
                and role in ("admin", "service_manager")
            ),
            ##
            "reopen_issue": lambda role, issue: bool(issue.closed),
            ##
            "update_issue": lambda role, issue: not issue.closed,
        }

        if action not in authorizations:
            raise ValueError("Unexpected action: {}".format(action))

        return authorizations[action](self.name, **kwargs)

    def get_default_url(self):
        urls = {
            "admin": "issue.index",
            "it_manager": "issue.index",
            "it_technician": "issue.index",
            "service_agent": "issue.index",
            "service_manager": "issue.index",
            "teacher": "issue.create",
        }
        self.validate_role(urls)
        return urls[self.name]

    def get_issue_type(self):
        if "issue_type" in request.cookies:
            return request.cookies.get("issue_type")

        issue_types = {
            "admin": None,
            "it_manager": "computer",
            "it_technician": "computer",
            "service_agent": "other",
            "service_manager": "other",
            "teacher": None,
        }
        self.validate_role(issue_types)
        return issue_types[self.name]

    def get_urls(self):
        urls = {
            "admin": [
                {"text": _l("Issues"), "endpoint": "issue.index"},
                {"text": _l("Users"), "endpoint": "user.index"},
            ],
            "it_manager": [
                {"text": _l("Issues"), "endpoint": "issue.index"},
                {"text": _l("IT Technicians"), "endpoint": "user.index"},
            ],
            "it_technician": [{"text": _l("Issues"), "endpoint": "issue.index"}],
            "service_agent": [{"text": _l("Issues"), "endpoint": "issue.index"}],
            "service_manager": [
                {"text": _l("Issues"), "endpoint": "issue.index"},
                {"text": _l("Service Agents"), "endpoint": "user.index"},
            ],
            "teacher": [{"text": _l("Issues"), "endpoint": "issue.index"}],
        }

        self.validate_role(urls)
        urls = urls[self.name]
        for url in urls:
            if "values" not in url:
                url["values"] = {}
        return urls

    def get_user_role(self):
        if "user_role" in request.cookies:
            return request.cookies.get("user_role")

        user_roles = {
            "admin": None,
            "it_manager": "it_technician",
            "service_manager": "service_agent",
            # "it_technician": N/A,
            # "service_agent": N/A,
            # "teacher": N/A,
        }
        self.validate_role(user_roles)
        return user_roles[self.name]

    def validate_role(self, urls):
        if self.name not in urls:
            raise ValueError("Unexpected role: {}".format(self.name))


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
