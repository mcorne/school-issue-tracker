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
    # Not using the login_required decorator so the login message is not displayed.
    # The login message is unwanted when a user click on a link to the app.
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))

    query = Issue.query
    type = request.args.get("type")
    if type:
        query = query.filter_by(type=type)
    issues = query.all()
    return render_template("issue/index.html", issues=issues)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = IssueForm()
    if form.validate_on_submit():
        issue = Issue(
            computer_number=form.computer_number.data,
            description=form.description.data,
            location=form.location.data,
            site=form.site.data,
            title=form.title.data,
            type=form.type.data,
            user_id=current_user.id,
            username=Issue.get_username(),
        )
        db.session.add(issue)
        db.session.commit()
        return redirect(url_for("issue.index"))

    return render_template("issue/create.html", form=form)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    issue = Issue.query.get_or_404(id)
    if not issue.username:
        issue.username = issue.user.username
    messages = issue.messages.all()
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            content=form.content.data,
            issue_id=id,
            user_id=current_user.id,
            username=Issue.get_username(),
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("issue.update", id=id))

    return render_template(
        "issue/update.html", form=form, id=id, issue=issue, messages=messages
    )
