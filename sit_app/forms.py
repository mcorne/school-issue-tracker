from enum import Enum

from flask_babel import lazy_gettext as _l
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
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    submit = SubmitField(_l("Log In"))
    username = StringField(_l("Username"), validators=[DataRequired()])


class PostForm(FlaskForm):
    body = TextAreaField(_l("Body"))
    submit = SubmitField(_l("Save"))
    title = StringField(_l("Title"), validators=[DataRequired()])


class Role(Enum):
    admin = _l("Administrator")
    teacher = _l("Teacher")
    it_technician = _l("IT Technician")
    it_manager = _l("IT Manager")
    service_agent = _l("Service Agent")
    service_manager = _l("Service Manager")

    @classmethod
    def coerce(cls, value):
        if isinstance(value, Role):
            value = value.name
        return value

    @classmethod
    def get_choices(cls):
        choices = [("", _l("-- Choose a role --"))] + [
            (role.name, role.value) for role in cls.__members__.values()
        ]
        return choices


class RegisterForm(FlaskForm):
    generic = BooleanField(_l("Generic Account"))
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    role = SelectField(
        _l("Role"),
        choices=Role.get_choices(),
        coerce=Role.coerce,
        validators=[DataRequired()],
    )
    submit = SubmitField(_l("Save"))
    username = StringField(_l("Username"), validators=[DataRequired()])


class UpdateForm(RegisterForm):
    disabled = BooleanField(_l("Account Disabled"))
    password = PasswordField(_l("Password (leave blank if unchanged)"))
