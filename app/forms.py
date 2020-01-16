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
    computer_number = StringField(_l("Computer Number (if applicable)"))
    description = TextAreaField(_l("Description"))
    location = StringField(
        _l("Location (classroom, building, outside etc.)"), validators=[DataRequired()]
    )
    site = RadioField(
        _l("Site"),
        choices=Site.get_choices(),
        coerce=Site.coerce,
        validators=[DataRequired()],
    )
    submit = SubmitField(_l("Save"))
    title = StringField(_l("Subject"), validators=[DataRequired()])
    type = RadioField(
        _l("Type"),
        choices=Type.get_choices(),
        coerce=Type.coerce,
        validators=[DataRequired()],
    )


class LoginForm(FlaskForm):
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    submit = SubmitField(_l("Log In"))
    username = StringField(_l("Username"), validators=[DataRequired()])


class RegisterForm(FlaskForm):
    generic = BooleanField(_l("Generic Account"))
    password = PasswordField(_l("Password"), validators=[DataRequired()],)
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

    def set_password_required(self):
        self.password.label.text = _l("Password")
        self.password.validators.append(DataRequired())
