from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_babel import _
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from app import db
from app.forms import IssueForm, MessageForm
from app.models.orm import Issue, Message, User

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


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    issue = Issue.query.get_or_404(id)
    messages = issue.messages.all()  # TODO: fix !!!
    form = MessageForm()
    if form.validate_on_submit():
        if current_user.generic:  # TODO: refactor !!!
            username = session.get("username")
        else:
            username = None
        message = Message(
            content=form.content.data,
            issue_id=id,
            user_id=current_user.id,
            username=username,
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("issue.update", id=id))

    return render_template("issue/update.html", form=form, id=id)
