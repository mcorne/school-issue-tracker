from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    password = PasswordField(lazy_gettext("Password"), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext("Log In"))
    username = StringField(lazy_gettext("Username"), validators=[DataRequired()])


class PostForm(FlaskForm):
    body = TextAreaField(lazy_gettext("Body"))
    submit = SubmitField(lazy_gettext("Save"))
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])


class RegisterForm(FlaskForm):
    password = PasswordField(lazy_gettext("Password"), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext("Register"))
    username = StringField(lazy_gettext("Username"), validators=[DataRequired()])
