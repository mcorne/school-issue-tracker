from datetime import datetime
from sit_app import db2


class User(db2.Model):
    id = db2.Column(db2.Integer, primary_key=True)
    username = db2.Column(db2.Text, unique=True, nullable=False)
    password = db2.Column(db2.Text, unique=True, nullable=False)
    password2 = db2.Column(db2.Text, unique=True, nullable=False)

    posts = db2.relationship("Post", back_populates="author", lazy="dynamic")


class Post(db2.Model):
    id = db2.Column(db2.Integer, primary_key=True)
    author_id = db2.Column(db2.Integer, db2.ForeignKey("user.id"))
    created = db2.Column(db2.DateTime, nullable=False, default=datetime.utcnow)
    title = db2.Column(db2.Text, nullable=False)
    body = db2.Column(db2.Text, nullable=False)

    author = db2.relationship("User", back_populates="posts")
