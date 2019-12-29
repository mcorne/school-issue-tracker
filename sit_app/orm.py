from datetime import datetime
from sit_app import db

db.Model.__table_args__ = {"sqlite_autoincrement": True}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship("Post", back_populates="author", lazy="dynamic")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created = db.Column(db.DateTime,
                         nullable=False,
                         server_default=db.text("CURRENT_TIMESTAMP"))
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)

    author = db.relationship("User", back_populates="posts")
