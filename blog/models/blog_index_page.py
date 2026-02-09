from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField

from core.models import HeadlessPage


class BlogIndexPage(HeadlessPage):
    intro = models.TextField(blank=True)

    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogPage"]

    content_panels = HeadlessPage.content_panels + [
        FieldPanel("intro"),
    ]

    api_fields = [
        APIField("intro"),
    ]
