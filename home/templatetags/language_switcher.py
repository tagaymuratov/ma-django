from django import template
from wagtail.models import Locale, Page

register = template.Library()


@register.simple_tag(takes_context=True)
def get_language_pages(context):
    request = context["request"]
    page = context.get("page")

    locales = Locale.objects.all()

    result = []

    for locale in locales:
        url = None

        if page:
            translation = page.get_translation_or_none(locale)

            if translation:
                url = translation.url

        if not url:
            root = Page.objects.filter(locale=locale, depth=2).first()
            if root:
                url = root.url

        result.append({
            "code": locale.language_code,
            "url": url
        })

    return result