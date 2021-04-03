from urllib.parse import urljoin

from django.conf import settings
from django.utils.encoding import iri_to_uri


def build_absolute_uri(location):
    # type: (str) -> str
    host = "example.com"
    protocol = "https" if settings.ENABLE_SSL else "http"
    current_uri = "%s://%s" % (protocol, host)
    location = urljoin(current_uri, location)
    return iri_to_uri(location)
