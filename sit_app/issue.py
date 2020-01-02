from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from sit_app import db
from sit_app.orm import Post, User

bp = Blueprint("issue", __name__)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("issue.index"))

    return render_template("issue/create.html")


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("issue.index"))


@bp.route("/")
def index():
    posts = Post.query.all()
    return render_template("issue/index.html", posts=posts)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = Post.query.get(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for("issue.index"))

    return render_template("issue/update.html", post=post)
