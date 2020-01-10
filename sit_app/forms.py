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

from sit_app.user import Role


class LoginForm(FlaskForm):
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    submit = SubmitField(_l("Log In"))
    username = StringField(_l("Username"), validators=[DataRequired()])


class PostForm(FlaskForm):
    body = TextAreaField(_l("Body"))
    submit = SubmitField(_l("Save"))
    title = StringField(_l("Title"), validators=[DataRequired()])


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
