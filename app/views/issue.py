from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_babel import _
from flask_login import current_user, login_required
from sqlalchemy import desc, func, text
from werkzeug.exceptions import abort

from app import db
from app.decorators import roles_required
from app.forms import IssueForm, MessageForm
from app.helpers import redirect_unauthorized_action
from app.models.issue import Type
from app.models.orm import Issue, Message, User

bp = Blueprint("issue", __name__)


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
        content = _("Changed to technical issue")
        issue.type = "other"
        notification = _("Issue changed to technical issue with success")
    else:
        if not current_user.role.authorized("change_to_computer_issue", issue=issue):
            return redirect_unauthorized_action()
        content = _("Changed to computer issue")
        issue.type = "computer"
        notification = _("Issue changed to computer issue with success")

    issue.reset_processing()
    Message.add_message(content, issue_id=id)
    db.session.commit()
    flash(notification)
    return redirect(url_for("issue.index"))


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
        flash(_("New issue created with success"))
        return redirect(url_for("issue.index"))

    return render_template("issue/create.html", form=form)


@bp.route("/")
def index():
    # Not using the login_required decorator so the login message is not displayed.
    # The login message is unwanted when a user click on a link to the app.
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))

    query = Issue.query
    type = current_user.role.get_issue_type()
    if type:
        query = query.filter_by(type=type)
    # query = query.order_by(desc(func.ifnull("updated", "created"))) # does not actually sort result!
    issues = query.order_by(text("IFNULL(updated, created) DESC")).all()
    return render_template("issue/index.html", issues=issues)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    issue = Issue.query.get_or_404(id)
    if not issue.username:
        issue.username = issue.user.username
    messages = issue.messages.all()

    form = MessageForm()
    if form.validate_on_submit():
        content = form.content.data
        if content:
            Message.add_message(content, issue_id=id)

        if form.close.data:
            if not current_user.role.authorized("close_issue", issue=issue):
                return redirect_unauthorized_action()
            Message.add_message(_("Closing of the issue"), issue_id=id)
            issue.closed = datetime.utcnow()
            issue.reset_processing()
            flash(_("Issue closed with success"))
        elif form.reopen.data:
            if not current_user.role.authorized("reopen_issue", issue=issue):
                return redirect_unauthorized_action()
            Message.add_message(_("Reopening of the issue"), issue_id=id)
            issue.closed = None
            issue.reset_processing()
            flash(_("Issue reopened with success"))
        else:
            if not current_user.role.authorized("update_issue", issue=issue):
                return redirect_unauthorized_action()
            issue.set_processing()
            flash(_("Issue updated with success"))

        db.session.commit()
        return redirect(url_for("issue.index"))

    return render_template(
        "issue/update.html", form=form, id=id, issue=issue, messages=messages
    )
