from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SeoConfig(AppConfig):
    name = "awesomeblog.seo"
    verbose_name = _("Seo")
