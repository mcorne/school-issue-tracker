from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_babel import _
from flask_login import login_required
from sqlalchemy import desc

from app import db
from app.decorators import roles_required
from app.forms import IpForm
from app.models.ip import IpTable
from app.models.orm import Ip
from app.models.user import Role

bp = Blueprint("ip", __name__, url_prefix="/ip")


@bp.route("/create", methods=("GET", "POST"))
@login_required
@roles_required(Role.admin)
def create():
    form = IpForm()
    if form.validate_on_submit():
        if not Ip.is_address_unique(form.address.data):
            flash(_("IP address already registered"), "error")
        else:
            ip = Ip(
                address=form.address.data,
                description=form.description.data,
                device=form.device.data,
                location=form.location.data,
                site=form.site.data,
                type=form.type.data,
            )
            db.session.add(ip)
            db.session.commit()
            flash(_("New IP created with success"))
            return redirect(url_for("ip.index", id=ip.id))

    return render_template("ip/edit.html", form=form)


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
@roles_required(Role.admin)
def delete(id):
    ip = Ip.query.get_or_404(id)
    db.session.delete(ip)
    db.session.commit()
    flash(_("IP address deleted with success"))

    return redirect(url_for("ip.index"))


@bp.route("/")
@login_required
@roles_required(Role.admin)
def index():
    sort = request.args.get("sort", "address")  # TODO: fix default sort !!!
    if sort not in IpTable._cols:
        sort = "address"
    reverse = request.args.get("direction", "asc") == "desc"
    order_by = desc(sort) if reverse else sort
    ips = Ip.query.order_by(order_by).all()
    table = IpTable(ips, sort_by=sort, sort_reverse=reverse)
    return render_template("ip/index.html", table=table)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
@roles_required(Role.admin)
def update(id):
    ip = Ip.query.get_or_404(id)
    form = IpForm(obj=ip)
    if form.validate_on_submit():
        if not Ip.is_address_unique(form.address.data, id):
            flash(_("IP address already used"), "error")
        else:
            form.populate_obj(ip)
            db.session.commit()
            flash(_("IP address updated with success"))
            return redirect(url_for("ip.index", id=ip.id))

    return render_template("ip/edit.html", form=form, id=id)
