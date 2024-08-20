import os
from flask import url_for
from urllib import parse as url_parse

activitypub_domain = os.environ.get('VITE_API_POINT')
server_scheme = url_parse.urlparse(activitypub_domain).scheme

def uri(name, *args):
    domain = activitypub_domain
    path = url_for(name, args=args, _scheme=server_scheme, _external=False)
    return "{domain}{path}".format(domain=domain, path=path)