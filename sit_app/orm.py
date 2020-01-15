from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import and_
from sqlalchemy.sql import expression
from werkzeug.security import check_password_hash, generate_password_hash

from sit_app import db
from sit_app.forms import Role

db.Model.__table_args__ = {"sqlite_autoincrement": True}
db.Model.created = db.Column(
    db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP")
)
db.Model.id = db.Column(db.Integer, primary_key=True)
db.Model.updated = db.Column(db.DateTime, onupdate=datetime.utcnow())


class Post(db.Model):
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    body = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)

    author = db.relationship("User", back_populates="posts")


class User(UserMixin, db.Model):
    generic = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    disabled = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship("Post", back_populates="author", lazy="dynamic")

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

    @classmethod
    def is_generic_user_password_unique(cls, password, id=None):
        """Check the generic account password is unique

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
