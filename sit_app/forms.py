from flask_babel import _, lazy_gettext
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(lazy_gettext("Username"), validators=[DataRequired()])
    password = PasswordField(lazy_gettext("Password"), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext("Log In"))


class RegisterForm(FlaskForm):
    username = StringField(lazy_gettext("Username"), validators=[DataRequired()])
    password = PasswordField(lazy_gettext("Password"), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext("Register"))
