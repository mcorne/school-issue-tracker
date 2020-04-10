from datetime import datetime

from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_babel import _
from flask_excel import make_response_from_array
from flask_login import current_user, login_required
from sqlalchemy import desc, func, text

from app import db
from app.decorators import roles_required
from app.forms import IssueForm, MessageForm
from app.helpers import fix_rows, redirect_unauthorized_action
from app.models.issue import Status, Type
from app.models.orm import Issue, Message
from app.models.user import Role

bp = Blueprint("issue", __name__)


@bp.route("/<int:id>/change_type")
@login_required
@roles_required(
    Role.admin,
    Role.it_support_2,
    Role.it_support_1,
    Role.facility_support_1,
    Role.facility_support_2,
)
def change_type(id):
    issue = Issue.query.get_or_404(id)
    if issue.type.is_it():
        if not current_user.authorized("change_to_facility_issue", issue):
            return redirect_unauthorized_action()
        content = _("Changed to facility management request")
        issue.type = Type.facility
        notification = _("Request changed to facility management request with success")
    else:
        if not current_user.authorized("change_to_it_issue", issue):
            return redirect_unauthorized_action()
        content = _("Changed to IT support request")
        issue.type = Type.it
        notification = _("Request changed to IT support request with success")

    issue.reset_pending()
    Message.add_message(content, issue_id=id)
    db.session.commit()
    flash(notification)
    return redirect(url_for("issue.index", issue_id=issue.id))


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
            status=Status.pending,
            title=form.title.data,
            type=form.type.data,
            user_id=current_user.id,
            username=Issue.get_username(),
        )
        db.session.add(issue)
        db.session.commit()
        flash(_("New request created with success"))
        return redirect(url_for("issue.index", issue_id=issue.id))

    return render_template("issue/create.html", form=form)


@bp.route("/download")
@login_required
@roles_required(Role.admin)
def download():
    headers = {
        "status": _("Status"),
        "type": _("Type"),
        "site": _("Site"),
        "location": _("Location"),
        "title": _("Subject"),
        "computer_number": _("Equipment"),
        "description": _("Description"),
        "username": _("Username"),
        "created": _("Creation date"),
        "updated": _("Last Update"),
        "closed": _("Close date"),
    }

    issue_type = current_user.role.get_issue_type()
    filter_by = {"type": issue_type} if issue_type != "all" else {}
    issues = (
        Issue.query.filter_by(**filter_by)
        .order_by("status", text("IFNULL(updated, created)"))  # like index
        .all()
    )
    fixed = fix_rows(issues, headers)
    return make_response_from_array(fixed, "xlsx", file_name=_("Requests"))


@bp.route("/")
@bp.route("/page/<int:page>")
def index(page=1):
    # Not using the login_required decorator so the login message is not displayed.
    # The login message is unwanted when a user click on a link to the app.
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))

    issue_type = current_user.role.get_issue_type()
    filter_by = {"type": issue_type} if issue_type != "all" else {}

    issue_sort = Issue.get_issue_sort()
    # desc(func.ifnull("updated", "created")) does not actually sort result!
    if issue_sort == "status":
        order_by = ["status", text("IFNULL(updated, created)")]  # like download
    else:
        order_by = [text("IFNULL(updated, created) DESC")]

    issue_page = (
        Issue.query.filter_by(**filter_by)
        .order_by(*order_by)
        .paginate(page, per_page=20)
    )
    issue_id = request.args.get("issue_id")
    template = render_template(
        "issue/index.html", issue_page=issue_page, issue_id=issue_id
    )

    response = make_response(template)
    max_age = 3600 * 24 * 30  # 30 days
    response.set_cookie("issue_sort", issue_sort, max_age)
    response.set_cookie("issue_type", issue_type, max_age)
    return response


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    issue = Issue.query.get_or_404(id)
    messages = issue.messages.all()

    form = MessageForm()
    if form.validate_on_submit():
        content = form.content.data
        if content:
            Message.add_message(content, issue_id=id)

        if form.close.data:
            if not current_user.authorized("close_issue", issue):
                return redirect_unauthorized_action()
            Message.add_message(_("Closing of the request"), issue_id=id)
            issue.set_closed()
            flash(_("Request closed with success"))
        elif form.reopen.data:
            if not current_user.authorized("reopen_issue", issue):
                return redirect_unauthorized_action()
            Message.add_message(_("Reopening of the request"), issue_id=id)
            issue.reset_pending()
            flash(_("Request reopened with success"))
        elif content:
            if not current_user.authorized("update_issue", issue):
                return redirect_unauthorized_action()
            issue.set_processing()
            flash(_("Request updated with success"))

        db.session.commit()
        return redirect(url_for("issue.index", issue_id=issue.id))

    return render_template(
        "issue/update.html", form=form, id=id, issue=issue, messages=messages
    )
