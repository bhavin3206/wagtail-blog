from django.core.management.base import BaseCommand
from django.utils import timezone
from wagtail.models import Page, Site

from blog.models import BlogIndexPage, BlogPage
from core.models import SiteBranding
from home.models import HomePage


class Command(BaseCommand):
    help = "Create example multisite structure and blog content."

    def handle(self, *args, **options):
        root = Page.get_first_root_node()

        site_definitions = [
            {
                "title": "Site A",
                "slug": "site-a",
                "hostname": "site-a.localhost",
                "brand_name": "Site A",
                "meta_keywords": "headless cms, wagtail, multisite",
                "posts": [
                    {
                        "title": "Hello from Site A",
                        "slug": "hello-from-site-a",
                        "seo_title": "Hello from Site A",
                        "schema_type": "BlogPosting",
                        "meta_keywords": "welcome, site a, headless",
                    },
                    {
                        "title": "Building a Headless CMS",
                        "slug": "building-a-headless-cms",
                        "seo_title": "Building a Headless CMS",
                        "schema_type": "Article",
                        "meta_keywords": "headless cms, wagtail, nextjs",
                        "body": [
                            (
                                "paragraph",
                                "Headless CMS separates content management from presentation, "
                                "letting your frontend evolve without touching the backend.",
                            ),
                            (
                                "heading",
                                {"text": "Why go headless?", "level": "h3"},
                            ),
                            (
                                "paragraph",
                                "Teams can ship a fast, modern UI in Next.js while Wagtail "
                                "handles rich editorial workflows, permissions, and drafts.",
                            ),
                            (
                                "quote",
                                "Content should be portable; experiences should be tailored.",
                            ),
                            (
                                "heading",
                                {"text": "Core building blocks", "level": "h3"},
                            ),
                            (
                                "paragraph",
                                "Model the content once with StreamField blocks, expose it "
                                "via the API, and reuse it across multiple sites.",
                            ),
                            (
                                "code",
                                {
                                    "language": "python",
                                    "code": "content = StreamField(BlogStreamBlock(), use_json_field=True)",
                                },
                            ),
                            (
                                "heading",
                                {"text": "Production checklist", "level": "h3"},
                            ),
                            (
                                "paragraph",
                                "Enable caching, set up webhooks for revalidation, and keep "
                                "media optimized with Wagtail image renditions.",
                            ),
                            (
                                "call_to_action",
                                {
                                    "text": "Read the architecture guide",
                                    "url": "https://example.com/architecture",
                                },
                            ),
                        ],
                    },
                    {
                        "title": "Why Multisite Matters",
                        "slug": "why-multisite-matters",
                        "seo_title": "Why Multisite Matters",
                        "schema_type": "Article",
                        "meta_keywords": "multisite, content, governance",
                    },
                ],
            },
            {
                "title": "Site B",
                "slug": "site-b",
                "hostname": "site-b.localhost",
                "brand_name": "Site B",
                "meta_keywords": "api first, nextjs, wagtail",
                "posts": [
                    {
                        "title": "Hello from Site B",
                        "slug": "hello-from-site-b",
                        "seo_title": "Hello from Site B",
                        "schema_type": "BlogPosting",
                        "meta_keywords": "welcome, site b, api",
                    },
                    {
                        "title": "Structured Content with StreamField",
                        "slug": "structured-content-with-streamfield",
                        "seo_title": "Structured Content with StreamField",
                        "schema_type": "Article",
                        "meta_keywords": "streamfield, wagtail, blocks",
                        "body": [
                            (
                                "paragraph",
                                "StreamField provides flexible, structured content without "
                                "locking editors into rigid templates.",
                            ),
                            (
                                "heading",
                                {"text": "Reusable blocks", "level": "h3"},
                            ),
                            (
                                "paragraph",
                                "Define blocks once and share them across different page types.",
                            ),
                            (
                                "code",
                                {
                                    "language": "python",
                                    "code": "class BlogStreamBlock(blocks.StreamBlock):\\n    heading = HeadingBlock()\\n    paragraph = ParagraphBlock()",
                                },
                            ),
                            (
                                "paragraph",
                                "Keep blocks shallow for performance and serialize with JSON.",
                            ),
                        ],
                    },
                    {
                        "title": "API-First Publishing",
                        "slug": "api-first-publishing",
                        "seo_title": "API-First Publishing",
                        "schema_type": "Article",
                        "meta_keywords": "api first, publishing, editorial",
                    },
                ],
            },
        ]

        for index, site_data in enumerate(site_definitions):
            home_page = self._get_or_create_home(root, site_data)
            blog_index = self._get_or_create_blog_index(home_page, site_data)
            blog_pages = []
            for post in site_data["posts"]:
                blog_pages.append(self._get_or_create_blog_page(blog_index, post))

            site, _ = Site.objects.update_or_create(
                hostname=site_data["hostname"],
                port=80,
                defaults={
                    "site_name": site_data["title"],
                    "root_page": home_page,
                    "is_default_site": index == 0,
                },
            )

            SiteBranding.objects.update_or_create(
                site=site,
                defaults={
                    "brand_name": site_data["brand_name"],
                    "meta_keywords": site_data.get("meta_keywords", ""),
                },
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Ready: {site.site_name} -> {home_page.slug}/{blog_index.slug}"
                )
            )

    def _get_or_create_home(self, root, site_data):
        existing = (
            HomePage.objects.child_of(root)
            .filter(slug=site_data["slug"])
            .first()
        )
        if existing:
            return existing

        home_page = HomePage(
            title=site_data["title"],
            slug=site_data["slug"],
            body=f"{site_data['title']} landing content.",
        )
        root.add_child(instance=home_page)
        home_page.save_revision().publish()
        return home_page

    def _get_or_create_blog_index(self, home_page, site_data):
        existing = (
            BlogIndexPage.objects.child_of(home_page)
            .filter(slug="blog")
            .first()
        )
        if existing:
            return existing

        blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
            intro=f"{site_data['title']} blog index.",
        )
        home_page.add_child(instance=blog_index)
        blog_index.save_revision().publish()
        return blog_index

    def _get_or_create_blog_page(self, blog_index, post_data):
        existing = (
            BlogPage.objects.child_of(blog_index)
            .filter(slug=post_data["slug"])
            .first()
        )
        content = post_data.get(
            "body",
            [
                ("heading", {"text": post_data["title"], "level": "h2"}),
                ("paragraph", "This is example content for the headless API."),
            ],
        )
        seo_title = post_data.get("seo_title", "")
        meta_keywords = post_data.get("meta_keywords", "")
        schema_type = post_data.get("schema_type", "Article")
        if existing:
            existing.title = post_data["title"]
            existing.excerpt = f"Sample excerpt for {post_data['title']}."
            existing.published_date = timezone.now().date()
            existing.content = content
            existing.meta_description = f"Example meta description for {post_data['title']}."
            existing.seo_title = seo_title
            existing.meta_keywords = meta_keywords
            existing.schema_type = schema_type
            existing.save_revision().publish()
            return existing

        blog_page = BlogPage(
            title=post_data["title"],
            slug=post_data["slug"],
            excerpt=f"Sample excerpt for {post_data['title']}.",
            published_date=timezone.now().date(),
            content=content,
            meta_description=f"Example meta description for {post_data['title']}.",
            seo_title=seo_title,
            meta_keywords=meta_keywords,
            schema_type=schema_type,
        )
        blog_index.add_child(instance=blog_page)
        blog_page.save_revision().publish()
        return blog_page
