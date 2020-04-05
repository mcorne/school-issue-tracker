from flask import request, url_for
from flask_babel import lazy_gettext as _l
from flask_table import Col, LinkCol, Table


class IpList(Table):
    classes = ["w3-table-all", "w3-hoverable"]
    address = LinkCol(
        _l("Address"),
        "ip.update",
        anchor_attrs={"class": "link"},
        attr="address",
        th_html_attrs={"class": "w3-blue w3-hover-gray"},
        url_kwargs=dict(id="id"),
    )  # TODO: escape with flask markup
    site = Col(_l("Site"), th_html_attrs={"class": "w3-blue w3-hover-gray"})
    location = Col(_l("Location"), th_html_attrs={"class": "w3-blue w3-hover-gray"})
    type = Col(_l("Type"), th_html_attrs={"class": "w3-blue w3-hover-gray"})
    device = Col(_l("Device"), th_html_attrs={"class": "w3-blue w3-hover-gray"})
    description = Col(
        _l("Description"), th_html_attrs={"class": "w3-blue w3-hover-gray"}
    )

    allow_sort = True
    no_items = ""

    def get_tr_attrs(self, ip):
        ip_id = request.args.get("ip_id")
        tr_attrs = {}
        if ip_id and ip.id == int(ip_id):
            tr_attrs["class"] = "w3-pale-green"
        return tr_attrs

    def sort_url(self, col_key, reverse=False):
        direction = "desc" if reverse else "asc"
        return url_for("ip.index", sort=col_key, direction=direction)
