from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class HeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True, max_length=120)
    level = blocks.ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        default="h2",
    )

    class Meta:
        icon = "title"
        label = "Heading"


class ParagraphBlock(blocks.RichTextBlock):
    class Meta:
        icon = "doc-full"
        label = "Paragraph"


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False, max_length=200)

    class Meta:
        icon = "image"
        label = "Image"


class QuoteBlock(blocks.BlockQuoteBlock):
    class Meta:
        icon = "openquote"
        label = "Quote"


class CodeBlock(blocks.StructBlock):
    language = blocks.CharBlock(required=False, max_length=30)
    code = blocks.TextBlock(required=True)

    class Meta:
        icon = "code"
        label = "Code"


class CallToActionBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True, max_length=80)
    url = blocks.URLBlock(required=True)

    class Meta:
        icon = "link"
        label = "Call to action"


class BlogStreamBlock(blocks.StreamBlock):
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    image = ImageBlock()
    quote = QuoteBlock()
    code = CodeBlock()
    embed = EmbedBlock()
    call_to_action = CallToActionBlock()

    class Meta:
        icon = "doc-full"
        label = "Blog body"
