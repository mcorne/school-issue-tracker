from flask_babel import _
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(_("Username"), validators=[DataRequired()])
    password = PasswordField(_("Password"), validators=[DataRequired()])
    submit = SubmitField(_("Log In"))
