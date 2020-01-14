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
        user = cls(
            password=generate_password_hash("123456"), role="admin", username="admin",
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def is_generic_user_password_unique(cls, password, id=None):
        users = cls.query.filter(
            and_(cls.disabled == False, cls.generic == True, cls.id != id)
        ).all()
        for user in users:
            if check_password_hash(user.password, password):
                return False
        return True

    @classmethod
    def is_username_unique(cls, username, id=None):
        if id is None:
            user = cls.query.filter_by(username=username).first()
        else:
            user = cls.query.filter(
                and_(cls.username == username, cls.id != id)
            ).first()
        return not user
