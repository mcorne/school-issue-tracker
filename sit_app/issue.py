from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from sit_app import db2
from sit_app.auth import login_required
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
            post = Post(title=title, body=body, author_id=g.user.id)
            db2.session.add(post)
            db2.session.commit()
            return redirect(url_for("issue.index"))

    return render_template("issue/create.html")


@bp.route("/<int:id>/delete", methods=("POST", ))
@login_required
def delete(id):
    post = Post.query.get(id)
    db2.session.delete(post)
    db2.session.commit()
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
            db2.session.commit()
            return redirect(url_for("issue.index"))

    return render_template("issue/update.html", post=post)
