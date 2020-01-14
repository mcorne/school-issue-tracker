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
from sqlalchemy import and_

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
        flash(_("Administrator may not be deleted."))
    else:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("auth.index"))


@bp.route("/login", methods=("GET", "POST"))
def login():  # TODO: fix to check password only for a generic account !!!
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(form.username.data, form.password.data)
        if not user:
            user = User.get_generic_account(form.password.data)
        if user:
            login_user(user)
            next = None  # session.get("next") TODO: restore/fix since always redirecting to same URL; auth/1/update!
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for("index"))

        flash(_("Invalid username or password"))

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@bp.route("/register", methods=("GET", "POST"))
@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not User.is_username_unique(form.username.data):
            flash(_("Username already registered"))
        elif form.generic.data and not User.is_generic_user_password_unique(
            form.password.data
        ):
            flash(_("Password already used for another generic account"))
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
            return redirect(url_for("auth.index"))

    return render_template("auth/register.html", form=form)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    user = User.query.get_or_404(id)
    form = UpdateForm(obj=user)
    if not form.disabled.data and (
        user.disabled or not user.generic and form.generic.data
    ):
        # force password to be reentered if user/account reenabled or changed to generic
        form.set_password_required()
    if form.validate_on_submit():
        if id == 1 and form.disabled.data:
            flash(_("Administrator may not be disabled."))
        elif not User.is_username_unique(form.username.data, id):
            flash(_("Username already used"))
        elif (
            form.password.data
            and not form.disabled.data
            and form.generic.data
            and not User.is_generic_user_password_unique(form.password.data, id)
        ):
            flash(_("Password already used for another generic account"))
        else:
            if not form.password.data:
                form.password.data = user.password
            else:
                form.password.data = generate_password_hash(form.password.data)
            form.populate_obj(user)
            db.session.commit()
            return redirect(url_for("auth.update", id=id))

    return render_template("auth/update.html", form=form, id=id)
