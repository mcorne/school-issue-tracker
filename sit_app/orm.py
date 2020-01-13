from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import and_
from sqlalchemy.sql import expression
from werkzeug.security import generate_password_hash

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

    def check_username_unique(self):
        if self.id is None:
            user = User.query.filter_by(username=self.username).first()
        else:
            user = User.query.filter(
                and_(
                    User.username == self.username, User.id != self.id
                )  # TODO: fix !!!
            ).first()
        return not user

    @classmethod
    def create_admin(cls):
        user = cls(
            password=generate_password_hash("123456"), role="admin", username="admin",
        )
        db.session.add(user)
        db.session.commit()
