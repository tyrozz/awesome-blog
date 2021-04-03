from django.contrib.sites.shortcuts import get_current_site

from ...core.utils import build_absolute_uri


def get_webpage_schema(request):
    """Build a schema.org representation of the website."""
    site = get_current_site(request)
    url = build_absolute_uri(location="/")
    data = {
        "@context": "http://schema.org",
        "@type": "WebSite",
        "url": url,
        "name": site.name,
        "description": site.settings.description,
    }

    return data
