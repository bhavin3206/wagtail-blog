from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from core.models import HeadlessPage


class HomePage(HeadlessPage):
    body = RichTextField(blank=True)

    content_panels = HeadlessPage.content_panels + [
        FieldPanel("body"),
    ]
