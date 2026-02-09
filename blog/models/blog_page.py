from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField

from core.models import HeadlessPage, SiteBranding
from .blocks import BlogStreamBlock


class BlogPage(HeadlessPage):
    excerpt = models.TextField(blank=True)
    published_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content = StreamField(
        BlogStreamBlock(),
        use_json_field=True,
        blank=True,
    )
    meta_description = models.TextField(
        blank=True,
        help_text="150-160 characters recommended. Leave blank to use excerpt.",
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords. Leave blank to use site defaults.",
    )
    og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Recommended size: 1200x630px.",
    )
    schema_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Examples: Article, BlogPosting, NewsArticle.",
    )

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []

    content_panels = HeadlessPage.content_panels + [
        FieldPanel("excerpt"),
        FieldPanel("hero_image"),
        FieldPanel("published_date"),
        FieldPanel("content"),
    ]

    promote_panels = HeadlessPage.promote_panels + [
        FieldPanel("meta_description"),
        FieldPanel("meta_keywords"),
        FieldPanel("og_image"),
        FieldPanel("schema_type"),
    ]

    def meta_keywords_effective(self):
        if self.meta_keywords:
            return self.meta_keywords
        site = self.get_site()
        if not site:
            return ""
        branding = SiteBranding.for_site(site)
        return branding.meta_keywords if branding and branding.meta_keywords else ""

    api_fields = [
        APIField("title"),
        APIField("slug"),
        APIField("excerpt"),
        APIField("published_date"),
        APIField("updated_at"),
        APIField("hero_image"),
        APIField("content"),
        APIField("seo_title"),
        APIField("meta_description"),
        APIField("meta_keywords"),
        APIField("meta_keywords_effective"),
        APIField("og_image"),
        APIField("schema_type"),
    ]
