from django.http import Http404
from wagtail.models import Page


class HeadlessPage(Page):
    class Meta:
        abstract = True

    def serve(self, request, *args, **kwargs):
        raise Http404()
