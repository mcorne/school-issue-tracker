from enum import Enum

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    password = PasswordField(lazy_gettext("Password"), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext("Log In"))
    username = StringField(lazy_gettext("Username"), validators=[DataRequired()])


class PostForm(FlaskForm):
    body = TextAreaField(lazy_gettext("Body"))
    submit = SubmitField(lazy_gettext("Save"))
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])


class Role(Enum):
    admin = lazy_gettext("Administrator")
    teacher = lazy_gettext("Teacher")
    it_technician = lazy_gettext("IT Technician")
    it_manager = lazy_gettext("IT Manager")
    service_agent = lazy_gettext("Service Agent")
    service_manager = lazy_gettext("Service Manager")

    @staticmethod
    def get_choices():
        choices = [("", "-- Choose a role --")] + [
            (name, member.value) for name, member in Role.__members__.items()
        ]
        return choices

    @classmethod
    def coerce(cls, value):
        if isinstance(value, Role):
            value = value.name
        return value


class RegisterForm(FlaskForm):
    generic = BooleanField(lazy_gettext("Generic"))
    password = PasswordField(lazy_gettext("Password"), validators=[DataRequired()])
    role = SelectField(
        lazy_gettext("Role"),
        choices=Role.get_choices(),
        coerce=Role.coerce,
        validators=[DataRequired()],
    )
    submit = SubmitField(lazy_gettext("Register"))
    username = StringField(lazy_gettext("Username"), validators=[DataRequired()])
