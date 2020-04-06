from flask import request, url_for
from flask_babel import lazy_gettext as _l
from flask_table import LinkCol, Table

from app.models.common import MyLinkCol


class IpLinkCol(MyLinkCol):
    def __init__(self, name, attr, **kwargs):
        super().__init__(attr=attr, endpoint="ip.update", name=name, **kwargs)


class IpList(Table):
    classes = ["w3-table-all", "w3-hoverable"]
    site = IpLinkCol(_l("Site"), "site")
    location = IpLinkCol(_l("Location"), "location")
    type = IpLinkCol(_l("Type"), "type")
    device = IpLinkCol(_l("Device"), "device")
    address = IpLinkCol(_l("Address"), "address")
    description = IpLinkCol(_l("Description"), "description")

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
