import functools

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_babel import _
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from sit_app import db
from sit_app.forms import LoginForm, RegisterForm, UpdateForm
from sit_app.orm import User
from sit_app.user import UserList
from sit_app.helpers import is_safe_url

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/")
@login_required
def index():
    users = User.query.all()
    return render_template("auth/index.html", table=UserList(users))


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
def delete(id):
    user = User.query.get_or_404(id)
    if id == 1:
        flash(_("The administrator may not be deleted."))
    else:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("auth.index"))


@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data, disabled=False).first()

        if user is None:
            error = _("Incorrect username")
        elif not check_password_hash(user.password, form.password.data):
            error = _("Incorrect password")

        if error is None:
            login_user(user)
            next = None  # session.get("next") TODO: restore/fix since always redirecting to same URL; auth/1/update!
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for("index"))

        flash(error)

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@bp.route("/register", methods=("GET", "POST"))
def register():
    # TODO: check teacher password is unique
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is not None:
            flash(_("User name already registered!"))
        else:
            password = generate_password_hash(form.password.data)
            user = User(
                generic=form.generic.data,
                password=password,
                role=form.role.data,
                username=form.username.data,
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    user = User.query.get_or_404(id)
    form = UpdateForm(obj=user)
    if form.validate_on_submit():
        if id == 1 and form.disabled.data is True:
            flash(_("The administrator may not be disabled."))
        elif User.query.filter_by(username=form.username.data).first() is not None:
            # TODO: add id != id !!!
            flash(_("The user name must be unique."))
        if not form.password.data:
            form.password.data = user.password
        else:
            form.password.data = generate_password_hash(form.password.data)
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("auth.update", id=id))

    return render_template("auth/register.html", form=form, id=id)
