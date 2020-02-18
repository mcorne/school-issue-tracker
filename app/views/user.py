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
from sqlalchemy import and_, desc
from werkzeug.security import generate_password_hash

from app import db
from app.forms import LoginForm, UserCreateForm, UserUpdateForm
from app.helpers import is_safe_url
from app.models.orm import User
from app.models.user import UserList

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/")
@login_required
def index():
    sort = request.args.get("sort", "username")
    reverse = request.args.get("direction", "asc") == "desc"
    if reverse:
        sort = desc(sort)
    users = User.query.order_by(sort).all()
    table = UserList(users, sort_by=sort, sort_reverse=reverse)
    return render_template("user/index.html", table=table)


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
def delete(id):
    user = User.query.get_or_404(id)
    if user.is_original_admin():
        flash(_("Administrator cannot be deleted"))
    elif user.has_issues():
        flash(_("User with issues cannot be deleted"))
    else:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("user.index"))


@bp.route("/login", methods=("GET", "POST"))
def login():
    session["username"] = None
    session["urls"] = {}
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(form.username.data, form.password.data)
        if not user:
            user = User.get_generic_account(form.password.data)
            if user:
                user.username = form.username.data
        if user:
            login_user(user)
            session["username"] = user.username
            session["urls"] = user.role.get_urls()

            next = None  # session.get("next") TODO: restore/fix since always redirecting to same URL; user/1/update!
            if not is_safe_url(next):
                return abort(400)
            if next:
                return redirect(next)

            url = user.role.get_default_url()
            location = url_for(url)
            return redirect(location)

        flash(_("Invalid username or password"))

    return render_template("user/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    session.pop("urls", None)
    session.pop("username", None)
    logout_user()
    return redirect(url_for("user.login"))


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = UserCreateForm()
    if form.validate_on_submit():
        if not User.is_username_unique(form.username.data):
            flash(_("Username already registered"))
        elif not User.is_generic_user_password_unique(form.password.data):
            flash(_("Password already used for a generic account"))
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
            return redirect(url_for("user.index"))

    return render_template("user/edit.html", form=form)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    user = User.query.get_or_404(id)
    has_issues = user.has_issues()
    form = UserUpdateForm(obj=user)
    if not form.disabled.data and (
        user.disabled or not user.generic and form.generic.data
    ):
        # Force the password to be reentered if the user/account is reenabled or changed to generic
        form.set_password_required()
    if form.validate_on_submit():
        if user.is_original_admin() and form.disabled.data:
            flash(_("Administrator may not be disabled"))
        elif not User.is_username_unique(form.username.data, id):
            flash(_("Username already used"))
        elif (
            form.password.data
            and not form.disabled.data
            and not User.is_generic_user_password_unique(form.password.data, id)
        ):
            flash(_("Password already used for a generic account"))
        else:
            if not form.password.data:
                form.password.data = user.password
            else:
                form.password.data = generate_password_hash(form.password.data)
            form.populate_obj(user)
            db.session.commit()
            return redirect(url_for("user.update", id=id))

    return render_template("user/edit.html", form=form, has_issues=has_issues, id=id)
