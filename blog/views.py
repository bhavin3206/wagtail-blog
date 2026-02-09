from django.http import JsonResponse
from django.views.decorators.http import require_GET
from wagtail.models import Site

from .models import BlogPage

@require_GET
def blog_list_api(request):
    site = Site.find_for_request(request)
    if site:
        blogs = (
            BlogPage.objects.descendant_of(site.root_page)
            .live()
            .public()
            .order_by("-published_date")
        )
    else:
        blogs = BlogPage.objects.live().public().order_by("-published_date")

    data = []
    for blog in blogs:
        body_blocks = []
        for block in blog.content:
            if block.block_type == "heading":
                body_blocks.append(
                    {
                        "type": "heading",
                        "value": {
                            "text": block.value.get("text"),
                            "level": block.value.get("level"),
                        },
                    }
                )
            elif block.block_type == "paragraph":
                body_blocks.append(
                    {
                        "type": "paragraph",
                        "value": (
                            block.value.source
                            if hasattr(block.value, "source")
                            else str(block.value)
                        ),
                    }
                )
            elif block.block_type == "image":
                image_obj = block.value.get("image")
                body_blocks.append(
                    {
                        "type": "image",
                        "value": {
                            "id": image_obj.id if image_obj else None,
                            "title": image_obj.title if image_obj else None,
                            "url": image_obj.file.url if image_obj else None,
                            "caption": block.value.get("caption"),
                        },
                    }
                )
            elif block.block_type == "quote":
                body_blocks.append({"type": "quote", "value": block.value})
            elif block.block_type == "code":
                body_blocks.append(
                    {
                        "type": "code",
                        "value": {
                            "language": block.value.get("language"),
                            "code": block.value.get("code"),
                        },
                    }
                )
            elif block.block_type == "embed":
                body_blocks.append({"type": "embed", "value": block.value})
            elif block.block_type == "call_to_action":
                body_blocks.append(
                    {
                        "type": "call_to_action",
                        "value": {
                            "text": block.value.get("text"),
                            "url": block.value.get("url"),
                        },
                    }
                )

        data.append({
            "id": blog.id,
            "title": blog.title,
            "slug": blog.slug,
            "excerpt": blog.excerpt,
            "published_date": blog.published_date,
            "updated_at": blog.updated_at,
            "hero_image": blog.hero_image_id,
            "seo_title": blog.seo_title,
            "meta_description": blog.meta_description,
            "meta_keywords": blog.meta_keywords_effective(),
            "body": body_blocks,
        })
    return JsonResponse(
        {
            "site": {
                "id": site.id if site else None,
                "name": site.site_name if site else None,
                "hostname": site.hostname if site else None,
            },
            "blogs": data,
        }
    )
