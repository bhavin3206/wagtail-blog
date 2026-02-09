from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting
class SiteBranding(BaseSiteSetting):
    brand_name = models.CharField(max_length=120)
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords for default SEO.",
    )
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("brand_name"),
        FieldPanel("meta_keywords"),
        FieldPanel("logo"),
    ]

    api_fields = [
        APIField("brand_name"),
        APIField("meta_keywords"),
        APIField("logo"),
    ]
