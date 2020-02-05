from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired

from app.models.issue import Site, Type
from app.models.user import Role


class IssueForm(FlaskForm):
    computer_number = StringField(_l("Equipment Number (if applicable)"))
    description = TextAreaField(_l("Description"))
    location = StringField(
        _l("Location (classroom, building, outside etc.)"), validators=[DataRequired()]
    )
    site = RadioField(
        _l("Site"),
        choices=Site.get_options(),
        coerce=Site.coerce,
        validators=[DataRequired()],
    )
    submit = SubmitField(_l("Save"))
    title = StringField(_l("Subject"), validators=[DataRequired()])
    type = RadioField(
        _l("Type"),
        choices=Type.get_options(),
        coerce=Type.coerce,
        validators=[DataRequired()],
    )


class LoginForm(FlaskForm):
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    submit = SubmitField(_l("Log In"))
    username = StringField(_l("Username"), validators=[DataRequired()])


class MessageForm(FlaskForm):
    content = TextAreaField(_l("Content"))
    submit = SubmitField(_l("Save"))


class UserCreateForm(FlaskForm):
    generic = BooleanField(_l("Generic Account"))
    password = PasswordField(_l("Password"), validators=[DataRequired()],)
    role = SelectField(
        _l("Role"),
        choices=Role.get_options(_l("-- Choose a role --")),
        coerce=Role.coerce,
        validators=[DataRequired()],
    )
    submit = SubmitField(_l("Save"))
    username = StringField(_l("Username"), validators=[DataRequired()])


class UserUpdateForm(UserCreateForm):
    disabled = BooleanField(_l("Account Disabled"))
    password = PasswordField(_l("Password (leave blank if unchanged)"))

    def set_password_required(self):
        self.password.label.text = _l("Password")
        self.password.validators.append(DataRequired())
