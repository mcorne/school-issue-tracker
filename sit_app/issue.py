from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_babel import _
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from sit_app import db
from sit_app.forms import PostForm
from sit_app.orm import Post, User

bp = Blueprint("issue", __name__)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, body=form.body.data, author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("issue.index"))

    return render_template("issue/create.html", form=form)


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
    form = PostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for("issue.index"))

    return render_template("issue/update.html", form=form, id=id)
