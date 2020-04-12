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
from wtforms.validators import DataRequired, EqualTo, IPAddress

from app.filters import fix_nl, strip
from app.helpers import convert_to_sortable_ascii
from app.models.issue import Site, Type
from app.models.user import Role


class MySelectField(SelectField):
    def __init__(self, keep_first_choice_first=True, **kwargs):
        self.keep_first_choice_first = keep_first_choice_first
        super().__init__(**kwargs)

    def __call__(self, **kwargs):
        if self.keep_first_choice_first:
            first_choice = self.choices.pop(0)
        self.choices = sorted(
            self.choices, key=lambda option: convert_to_sortable_ascii(str(option[1]))
        )
        if self.keep_first_choice_first:
            self.choices.insert(0, first_choice)

        return super().__call__(**kwargs)


class IpForm(FlaskForm):
    address = StringField(
        _l("IP address"), filters=[strip], validators=[DataRequired(), IPAddress()]
    )
    description = TextAreaField(_l("Description"), filters=[fix_nl])
    device = StringField(
        _l("Device (model etc.)"), filters=[strip], validators=[DataRequired()]
    )
    location = StringField(
        _l("Location (classroom etc.)"), filters=[strip], validators=[DataRequired()]
    )
    site = RadioField(
        _l("Site"),
        choices=Site.get_options(),
        coerce=Site.coerce,
        validators=[DataRequired()],
    )
    submit = SubmitField(_l("Save"))
    type = StringField(
        _l("Type (computer, printer etc.)"),
        filters=[strip],
        validators=[DataRequired()],
    )


class IssueForm(FlaskForm):
    computer_number = StringField(
        _l("Equipment Number (if applicable)"), filters=[strip]
    )
    description = TextAreaField(_l("Description"), filters=[fix_nl])
    location = StringField(
        _l("Location (classroom, building, outside etc.)"),
        filters=[strip],
        validators=[DataRequired()],
    )
    site = RadioField(
        _l("Site"),
        choices=Site.get_options(),
        coerce=Site.coerce,
        validators=[DataRequired()],
    )
    submit = SubmitField(_l("Save"))
    title = StringField(_l("Subject"), filters=[strip], validators=[DataRequired()])
    type = RadioField(
        _l("Type"),
        choices=Type.get_options(),
        coerce=Type.coerce,
        validators=[DataRequired()],
    )


class LoginForm(FlaskForm):
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    submit = SubmitField(_l("Log In"))
    username = StringField(_l("Username"), filters=[strip], validators=[DataRequired()])


class MessageForm(FlaskForm):
    content = TextAreaField(_l("Message"), filters=[fix_nl])
    submit = SubmitField(_l("Save"))
    close = SubmitField(_l("Close"))
    reopen = SubmitField(_l("Reopen"))


class PasswordForm(FlaskForm):
    confirmed_password = PasswordField(
        _l("Confirm password"),
        validators=[
            DataRequired(),
            EqualTo("new_password", message=_l("Invalid password confirmation")),
        ],
    )
    current_password = PasswordField(
        _l("Current password"), validators=[DataRequired()]
    )
    new_password = PasswordField(_l("New password"), validators=[DataRequired()])
    submit = SubmitField(_l("Save"))


class UserCreateForm(FlaskForm):
    generic = BooleanField(_l("Generic Account"))
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    role = MySelectField(
        _l("Role"),
        choices=Role.get_options(_l("-- Choose a role --")),
        coerce=Role.coerce,
        validators=[DataRequired()],
    )
    submit = SubmitField(_l("Save"))
    username = StringField(_l("Username"), filters=[strip], validators=[DataRequired()])


class UserUpdateForm(UserCreateForm):
    disabled = BooleanField(_l("Account Disabled"))
    password = PasswordField(_l("Password (leave blank if unchanged)"))

    def set_password_required(self):
        self.password.label.text = _l("Password")
        self.password.validators.append(DataRequired())
