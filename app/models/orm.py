from datetime import datetime

from flask import session
from flask_login import UserMixin, current_user
from sqlalchemy import and_
from sqlalchemy.sql import expression
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models.issue import Site, Type
from app.models.user import Role

db.Model.__table_args__ = {"sqlite_autoincrement": True}
db.Model.id = db.Column(db.Integer, primary_key=True)
db.Model.created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
db.Model.updated = db.Column(db.DateTime, onupdate=datetime.utcnow())


class Issue(db.Model):
    closed = db.Column(db.DateTime)
    computer_number = db.Column(db.Text)  # for computer related issues
    description = db.Column(db.Text)
    location = db.Column(db.Text, nullable=False)
    site = db.Column(db.Enum(Site), nullable=False)
    title = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum(Type), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    username = db.Column(db.Text)  # for generic accounts, null for regular users
    # links
    user = db.relationship("User", back_populates="issues")
    messages = db.relationship("Message", back_populates="issue", lazy="dynamic")

    @staticmethod
    def get_username():
        if current_user.generic:
            username = session.get("username")
        else:
            username = None
        return username


class Message(db.Model):
    content = db.Column(db.Text)
    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    username = db.Column(db.Text)  # for generic accounts, null for regular users
    # links
    issue = db.relationship("Issue", back_populates="messages")
    user = db.relationship("User", back_populates="messages")


class User(UserMixin, db.Model):
    generic = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    disabled = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    # links
    issues = db.relationship("Issue", back_populates="user", lazy="dynamic")
    messages = db.relationship("Message", back_populates="user", lazy="dynamic")

    @classmethod
    def create_admin(cls):
        """Create the administrator user"""
        user = cls(
            password=generate_password_hash("123456"), role="admin", username="admin"
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def get_generic_account(cls, password):
        """Return the generic account with the given password"""
        users = cls.query.filter(and_(cls.disabled == False, cls.generic == True)).all()
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
    def is_generic_user_password_unique(cls, password, id=None):
        """Check that the generic account password is unique

        Generic account passwords must be unique accross all passwords including user passwords.
        If a generic account and a user shared the same password, a user mistyping his/her username
        could possibly and wrongly login into a generic account.
        """
        users = cls.query.filter(and_(cls.disabled == False, cls.id != id)).all()
        for user in users:
            if check_password_hash(user.password, password):
                return False
        return True

    @classmethod
    def is_username_unique(cls, username, id=None):
        """Check that the username is unique"""
        user = cls.query.filter(and_(cls.username == username, cls.id != id)).first()
        return not user
