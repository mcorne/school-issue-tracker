from urllib.parse import urljoin, urlparse

from flask import Blueprint, request

# see https://github.com/fengsp/flask-snippets/blob/master/security/redirect_back.py
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc
