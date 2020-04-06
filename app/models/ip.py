from flask import request, url_for
from flask_babel import lazy_gettext as _l

from app.models.common import MyLinkCol, MyTable


class IpLinkCol(MyLinkCol):
    def __init__(self, name, attr, **kwargs):
        super().__init__(attr=attr, endpoint="ip.update", name=name, **kwargs)


class IpTable(MyTable):
    endpoint = "ip.index"
    site = IpLinkCol(_l("Site"), "site")
    location = IpLinkCol(_l("Location"), "location")
    type = IpLinkCol(_l("Type"), "type")
    device = IpLinkCol(_l("Device"), "device")
    address = IpLinkCol(_l("Address"), "address")
    description = IpLinkCol(_l("Description"), "description")
