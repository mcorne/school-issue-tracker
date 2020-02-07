from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_babel import _
from flask_login import current_user, login_required
from sqlalchemy import desc
from werkzeug.exceptions import abort

from app import db
from app.decorators import roles_required
from app.forms import IssueForm, MessageForm
from app.helpers import redirect_unauthorized_action
from app.models.issue import Type
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
    issues = query.order_by(desc("updated")).all()
    return render_template("issue/index.html", issues=issues)


@bp.route("/<int:id>/change_type")
@login_required
@roles_required(
    "admin", "it_manager", "it_technician", "service_agent", "service_manager"
)
def change_type(id):
    issue = Issue.query.get_or_404(id)
    if issue.type.name == "computer":
        if not current_user.role.authorized("change_to_technical_issue", issue=issue):
            return redirect_unauthorized_action()
        content = _("Issue changed to technical issue")
        issue.type = "other"
        notification = _("Issue changed to technical issue")
    else:
        if not current_user.role.authorized("change_to_computer_issue", issue=issue):
            return redirect_unauthorized_action()
        content = _("Issue changed to computer issue")
        issue.type = "computer"
        notification = _("Issue changed to computer issue")

    message = Message(
        content=content,
        issue_id=id,
        user_id=current_user.id,
        username=Issue.get_username(),
    )
    db.session.add(message)
    db.session.commit()
    flash(notification)
    # TODO: filter list according to role !!!
    return redirect(url_for("issue.index", id=id))


@bp.route("/<int:id>/close")
@login_required
@roles_required("admin", "it_manager", "service_manager")
def close(id):
    issue = Issue.query.get_or_404(id)
    if not current_user.role.authorized("close_issue", issue=issue):
        return redirect_unauthorized_action()

    issue.closed = datetime.utcnow()
    message = Message(
        content=_("Closing of the issue"),
        issue_id=id,
        user_id=current_user.id,
        username=Issue.get_username(),
    )
    db.session.add(message)
    db.session.commit()
    flash(_("Issue closed"))
    # TODO: filter list according to role !!!
    return redirect(url_for("issue.index", id=id))


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
        flash(_("New issue created"))
        return redirect(url_for("issue.index"))

    return render_template("issue/create.html", form=form)


@bp.route("/<int:id>/reopen")
@login_required
def reopen(id):
    issue = Issue.query.get_or_404(id)
    if not current_user.role.authorized("reopen_issue", issue=issue):
        return redirect_unauthorized_action()

    issue.closed = None
    message = Message(
        content=_("Reopening of the issue"),
        issue_id=id,
        user_id=current_user.id,
        username=Issue.get_username(),
    )
    db.session.add(message)
    db.session.commit()
    flash(_("Issue reopened"))
    # TODO: filter list according to role !!!
    return redirect(url_for("issue.index", id=id))


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
        flash(_("Issue updated"))
        return redirect(url_for("issue.update", id=id))

    return render_template(
        "issue/update.html", form=form, id=id, issue=issue, messages=messages
    )
