import functools

from flask import (
    Blueprint,
    abort,
    flash,
    g,
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
from sit_app.orm import User
from sit_app.helpers import is_safe_url

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = _("Incorrect username")
        elif not check_password_hash(user.password, password):
            error = _("Incorrect password")

        if error is None:
            login_user(user, remember=True)
            next = session.get("next")
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = _("Username is required")
        elif not password:
            error = _("Password is required")
        elif User.query.filter_by(username=username).first() is not None:
            error = _("User %(username)s already registered", username=username)

        if error is None:
            password = generate_password_hash(password)
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")
