from django.utils import timezone

from .blog_index_page import BlogIndexPage
from .blog_page import BlogPage


def today():
    return timezone.now().date()

__all__ = ["BlogIndexPage", "BlogPage", "today"]
