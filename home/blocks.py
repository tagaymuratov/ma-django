from wagtail import blocks

class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True, label="Button text")
    url = blocks.URLBlock(required=True, label="Link")

    class Meta:
        template = "blocks/button_block.html"
        icon = "link"
        label = "Button"