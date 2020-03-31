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
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import desc
from werkzeug.security import generate_password_hash

from app import db
from app.decorators import roles_required
from app.forms import LoginForm, UserCreateForm, UserUpdateForm
from app.helpers import is_safe_url
from app.models.orm import User
from app.models.user import Role, UserList

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/create", methods=("GET", "POST"))
@login_required
@roles_required(Role.admin)
def create():
    form = UserCreateForm()
    if form.validate_on_submit():
        if not User.is_username_unique(form.username.data):
            flash(_("Username already registered"), "error")
        elif not User.is_generic_user_password_unique(
            form.password.data, form.generic.data
        ):
            flash(_("Password already used for a generic account"), "error")
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
            flash(_("New user created with success"))
            return redirect(url_for("user.index", user_id=user.id))

    return render_template("user/edit.html", form=form)


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
@roles_required(Role.admin)
def delete(id):
    user = User.query.get_or_404(id)
    if user.is_original_admin():
        flash(_("Administrator cannot be deleted"), "error")
    elif user.has_issues():
        flash(_("User with issues cannot be deleted"), "error")
    else:
        db.session.delete(user)
        db.session.commit()
        flash(_("User deleted with success"))

    return redirect(url_for("user.index"))


@bp.route("/")
@login_required
@roles_required(Role.admin)
def index():
    sort = request.args.get("sort", "username")  # TODO: validate sort !!!
    reverse = request.args.get("direction", "asc") == "desc"
    order_by = desc(sort) if reverse else sort
    users = User.query.order_by(order_by).all()
    table = UserList(users, sort_by=sort, sort_reverse=reverse)
    return render_template("user/index.html", table=table)


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

            # TODO: restore/fix since always redirecting to same URL: user/1/update!
            next = None  # session.get("next")
            if not is_safe_url(next):
                return abort(400)
            if next:
                return redirect(next)

            url = user.role.get_default_url()
            location = url_for(url)
            return redirect(location)

        flash(_("Invalid username or password"), "error")

    return render_template("user/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    session.pop("urls", None)
    session.pop("username", None)
    logout_user()
    return redirect(url_for("user.login"))


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
@roles_required(Role.admin)
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
        if user.is_original_admin() and (
            form.disabled.data or form.role.data != Role.admin.name
        ):
            flash(
                _("Original administrator role may not be changed or disabled"), "error"
            )
        elif not User.is_username_unique(form.username.data, id):
            flash(_("Username already used"), "error")
        elif (
            form.password.data
            and not form.disabled.data
            and not User.is_generic_user_password_unique(
                form.password.data, form.generic.data, id
            )
        ):
            flash(_("Password already used for a generic account"), "error")
        else:
            if not form.password.data:
                form.password.data = user.password
            else:
                form.password.data = generate_password_hash(form.password.data)
            form.populate_obj(user)
            db.session.commit()
            flash(_("User updated with success"))
            return redirect(url_for("user.index", user_id=user.id))

    return render_template("user/edit.html", form=form, has_issues=has_issues, id=id)
