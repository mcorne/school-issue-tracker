from datetime import datetime

from flask import session
from flask_login import UserMixin, current_user
from sqlalchemy.sql import expression
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.helpers import get_arg_or_cookie
from app.models.issue import Site, Status, Type
from app.models.user import Role


class CommonColumns(object):
    __table_args__ = {"sqlite_autoincrement": True}
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Ip(CommonColumns, db.Model):
    __table_args__ = (
        db.Index("ip_default_sort", "site", "location", "type", "device"),
    )

    address = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.Text)
    device = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    site = db.Column(db.Enum(Site, length=100, native_enum=False), nullable=False)
    type = db.Column(db.Text, nullable=False)

    @classmethod
    def is_address_unique(cls, address, id=None):
        ip = cls.query.filter(cls.address == address, cls.id != id).first()
        return not ip


class Issue(CommonColumns, db.Model):
    __table_args__ = (
        db.Index("issue_default_sort", "type", "status", "updated", "created"),
    )

    closed = db.Column(db.DateTime)
    computer_number = db.Column(db.Text)  # for computer related issues
    description = db.Column(db.Text)
    location = db.Column(db.Text, nullable=False)
    site = db.Column(db.Enum(Site, length=100, native_enum=False), nullable=False)
    status = db.Column(
        # Store the status value (ex. "1") instead of the name (ex. "pending")
        # to be able to sort issues by status in the following order: pending, processing, closed
        # Cast the value to string to bypass the TypeError exception: "object of type 'int' has no len()"!
        db.Enum(Status, values_callable=lambda x: [str(e.value) for e in x]),
        nullable=False,
    )
    title = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum(Type, length=100, native_enum=False), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    username = db.Column(db.Text)  # Used only for generic accounts
    # Links
    user = db.relationship("User", back_populates="issues")
    messages = db.relationship("Message", back_populates="issue", lazy="dynamic")

    @staticmethod
    def get_issue_sort():
        issue_sort = get_arg_or_cookie("issue_sort")
        if issue_sort not in ("date", "status"):
            issue_sort = "date"
        return issue_sort

    @staticmethod
    def get_selected_site():
        site = get_arg_or_cookie("selected_site")
        if site not in ("all", "marie_curie", "molière"):
            site = "all"
        return site

    @staticmethod
    def get_username():
        if current_user.generic:
            username = session.get("username")
        else:
            username = None
        return username

    def is_closed(self):
        return self.status == Status.closed

    def is_processing(self):
        return self.status == Status.processing

    def opened_by_user(self):
        return current_user.id == self.user.id and (
            not current_user.generic
            # Ex. teacher that created the issue
            or self.username == session.get("username")
        )

    def reset_pending(self):
        self.closed = None
        self.status = Status.pending
        self.updated = datetime.utcnow()

    def set_closed(self):
        self.closed = datetime.utcnow()
        self.status = Status.closed
        self.updated = datetime.utcnow()

    def set_processing(self):
        if current_user.role.authorized("update_issue", self):
            self.status = Status.processing
        # Always set the updated date that would not be set (on update by default) if there is no change
        self.updated = datetime.utcnow()


db.Index("issue_user_id", Issue.user_id)


class Message(CommonColumns, db.Model):
    content = db.Column(db.Text)
    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    username = db.Column(db.Text)  # Used only for generic accounts
    # Links
    issue = db.relationship("Issue", back_populates="messages")
    user = db.relationship("User", back_populates="messages")

    @classmethod
    def add_message(cls, content, issue_id):
        message = cls(
            content=content,
            issue_id=issue_id,
            user_id=current_user.id,
            username=Issue.get_username(),
        )
        db.session.add(message)

    @classmethod
    def reopened_by_current_user(cls, issue):
        filter_by = dict(issue_id=issue.id, user_id=current_user.id)
        if current_user.generic:
            # Ex. teacher that reopened the issue
            filter_by["username"] = session.get("username")
        message = cls.query.filter_by(**filter_by).first()
        return bool(message)


db.Index("message_issue_id", Message.issue_id)
db.Index("message_user_id", Message.user_id)


class User(UserMixin, CommonColumns, db.Model):
    generic = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    disabled = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Enum(Role, length=100, native_enum=False), nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    # Links
    issues = db.relationship("Issue", back_populates="user", lazy="dynamic")
    messages = db.relationship("Message", back_populates="user", lazy="dynamic")

    def authorized(self, action, issue=None):
        if action == "change_password":
            return not current_user.generic

        if (
            action == "update_issue"
            and not issue.is_closed()
            and (issue.opened_by_user() or Message.reopened_by_current_user(issue))
        ):
            return True

        return self.role.authorized(action, issue)

    @classmethod
    def create_admin(cls):
        """Create the administrator user"""
        user = cls(
            password=generate_password_hash("123456"), role=Role.admin, username="admin"
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def get_generic_account(cls, password):
        """Return the generic account with the given password"""
        users = cls.query.filter_by(disabled=False, generic=True).all()
        for user in users:
            if check_password_hash(user.password, password):
                return user

    @classmethod
    def get_user(cls, username, password):
        """Return the user with the given username and password"""
        user = cls.query.filter_by(username=username, disabled=False).first()
        if user and check_password_hash(user.password, password):
            return user

    def has_issues(self):
        return bool(self.issues.first())

    @classmethod
    def is_generic_user_password_unique(cls, password, generic, id=None):
        """Check that the generic account password is unique

        Generic account passwords must be unique accross all passwords including user passwords.
        If a generic account and a user shared the same password, a user mistyping his/her username
        could possibly and wrongly login with a generic account.
        """
        filter = [cls.disabled == False]
        if id:
            filter.append(cls.id != id)
        if not generic:
            filter.append(cls.generic == True)
        users = cls.query.filter(*filter).all()

        for user in users:
            if check_password_hash(user.password, password):
                return False
        return True

    def is_original_admin(self):
        return self.id == 1

    @classmethod
    def is_username_unique(cls, username, id=None):
        user = cls.query.filter(cls.username == username, cls.id != id).first()
        return not user
