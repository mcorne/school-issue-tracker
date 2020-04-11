from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_babel import _
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import desc
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.decorators import roles_required
from app.forms import LoginForm, PasswordForm, UserCreateForm, UserUpdateForm
from app.helpers import redirect_unauthorized_action
from app.models.orm import User
from app.models.user import Role, UserTable

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
            return redirect(url_for("user.index", id=user.id))

    return render_template("user/edit.html", form=form)


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
@roles_required(Role.admin)
def delete(id):
    user = User.query.get_or_404(id)
    if user.is_original_admin():
        flash(_("Administrator cannot be deleted"), "error")
    elif user.has_issues():
        flash(_("Users with requests cannot be deleted"), "error")
    else:
        db.session.delete(user)
        db.session.commit()
        flash(_("User deleted with success"))

    return redirect(url_for("user.index"))


@bp.route("/")
@login_required
@roles_required(Role.admin)
def index():
    sort = request.args.get("sort", "username")
    if sort not in UserTable._cols:
        sort = "username"
    reverse = request.args.get("direction", "asc") == "desc"

    if sort == "role":
        role_sql, role_params = Role.get_sql_values()
        sql = (
            "SELECT user.*, roles.value AS role FROM user LEFT JOIN ("
            + role_sql
            + ") AS roles ON roles.name = user.role ORDER BY roles.value"
        )
        if reverse:
            sql += " DESC"
        users = db.engine.execute(sql, **role_params).fetchall()
    else:
        order_by = desc(sort) if reverse else sort
        users = User.query.order_by(order_by).all()

    table = UserTable(users, sort_by=sort, sort_reverse=reverse)
    return render_template("user/index.html", table=table)


@bp.route("/login", methods=("GET", "POST"))
def login():
    session["username"] = None
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
            url = user.role.get_default_url()
            location = url_for(url)
            return redirect(location)

        flash(_("Invalid username or password"), "error")

    return render_template("user/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    session.pop("username", None)
    logout_user()
    return redirect(url_for("user.login"))


@bp.route("/password", methods=("GET", "POST"))
@login_required
def password():
    if not current_user.authorized("change_password"):
        return redirect_unauthorized_action()

    id = current_user.id
    user = User.query.get_or_404(id)

    form = PasswordForm()
    if form.validate_on_submit():
        if not check_password_hash(user.password, form.current_password.data):
            flash(_("Incorrect current password"), "error")
        elif form.new_password.data != form.confirmed_password.data:
            flash(_("Invalid password confirmation"), "error")
        elif not User.is_generic_user_password_unique(
            form.new_password.data, user.generic, id
        ):
            flash(_("Password already used for a generic account"), "error")
        else:
            user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash(_("Password changed with success"))
            return redirect(url_for("user.logout"))

    return render_template("user/password.html", form=form)


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
            return redirect(url_for("user.index", id=user.id))

    return render_template("user/edit.html", form=form, has_issues=has_issues, id=id)
