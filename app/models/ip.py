from flask_babel import lazy_gettext as _l

from app.models.common import MyLinkCol, MyTable


class IpLinkCol(MyLinkCol):
    endpoint = "ip.update"


class IpTable(MyTable):
    endpoint = "ip.index"
    site = IpLinkCol(_l("Site"), "site")
    location = IpLinkCol(_l("Location"), "location")
    type = IpLinkCol(_l("Type"), "type")
    device = IpLinkCol(_l("Device"), "device")
    address = IpLinkCol(_l("IP address"), "address")
    description = IpLinkCol(_l("Description"), "description")
