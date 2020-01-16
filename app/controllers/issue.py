from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_babel import _
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from app import db
from app.forms import IssueForm
from app.models.orm import Issue, User

bp = Blueprint("issue", __name__)


@bp.route("/")
def index():
    issues = Issue.query.all()
    return render_template("issue/index.html", issues=issues)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = IssueForm()
    if form.validate_on_submit():
        if current_user.generic:
            username = session.get("username")
        else:
            username = None
        issue = Issue(
            computer_number=form.computer_number.data,
            description=form.description.data,
            location=form.location.data,
            site=form.site.data,
            title=form.title.data,
            type=form.type.data,
            username=username,
            user_id=current_user.id,
        )
        db.session.add(issue)
        db.session.commit()
        return redirect(url_for("issue.index"))

    return render_template("issue/create.html", form=form)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    issue = Issue.query.get_or_404(id)
    db.session.delete(issue)
    db.session.commit()
    return redirect(url_for("issue.index"))


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    issue = Issue.query.get_or_404(id)
    form = IssueForm(obj=issue)
    if form.validate_on_submit():
        form.populate_obj(issue)
        db.session.commit()
        return redirect(url_for("issue.index"))

    return render_template("issue/update.html", form=form, id=id)
