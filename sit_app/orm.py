from datetime import datetime

from flask_login import UserMixin

from sit_app import db
from sit_app.forms import Role

db.Model.__table_args__ = {"sqlite_autoincrement": True}
db.Model.id = db.Column(db.Integer, primary_key=True)


class Post(db.Model):
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    body = db.Column(db.Text, nullable=False)
    created = db.Column(
        db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP")
    )
    title = db.Column(db.Text, nullable=False)

    author = db.relationship("User", back_populates="posts")


class User(UserMixin, db.Model):
    generic = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Enum(Role), nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship("Post", back_populates="author", lazy="dynamic")
