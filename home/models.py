from urllib import request

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.models import Page
from wagtail.fields import StreamField

from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

class ContentMixin(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    preview = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,  
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField([
        ('rtfblock', RichTextBlock(features=[
            "h1","h2","h3","ol","ul","hr","blockquote","superscript","subscript","strikethrough","bold","italic","link"
        ], label="Текст")),
        ('imgblock', ImageChooserBlock(label="Изображение", template="blocks/image_block.html")),
        ('embedblock', EmbedBlock(label="Youtube", template="blocks/embed_block.html")),
    ], blank=True)

    class Meta:
        abstract = True

class HomePage(Page):
    max_count = 1
    subpage_types = ["EventIndexPage", "NewsIndexPage", "PodcastIndexPage", "CourseIndexPage", "AboutPage"]

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_title = models.CharField(max_length=255, blank=True, null=True)
    hero_subtitle = models.CharField(max_length=255, blank=True, null=True)

    content_panels = Page.content_panels + ["hero_image", "hero_title", "hero_subtitle"]

    def get_context(self, request):
        context = super().get_context(request)
        context["events"] = EventPage.objects.live().order_by("-first_published_at")[:4]
        context["events_link"] = EventIndexPage.objects.live().first()
        context["news"] = NewsPage.objects.live().order_by("-first_published_at")[:4]
        context["news_link"] = NewsIndexPage.objects.live().first()
        context["podcasts"] = PodcastPage.objects.live().order_by("-first_published_at")[:4]
        context["podcasts_link"] = PodcastIndexPage.objects.live().first()
        context["courses"] = CoursePage.objects.live().order_by("-first_published_at")[:4]
        context["courses_link"] = CourseIndexPage.objects.live().first()
        return context
    
class AboutPage(Page, ContentMixin):
    subpage_types = []
    parent_page_types = ["HomePage"]
    max_count = 1
    content_panels = Page.content_panels + ["body"]

class EventIndexPage(Page):
    subpage_types = ["EventPage"]
    parent_page_types = ["HomePage"]
    max_count = 1
    def get_context(self, request):
        context = super().get_context(request)
        return get_index_context(context, EventPage, request)

class NewsIndexPage(Page):
    subpage_types = ["NewsPage"]
    parent_page_types = ["HomePage"]
    max_count = 1
    def get_context(self, request):
        context = super().get_context(request)
        return get_index_context(context, NewsPage, request)

class PodcastIndexPage(Page):
    subpage_types = ["PodcastPage"]
    parent_page_types = ["HomePage"]
    max_count = 1
    def get_context(self, request):
        context = super().get_context(request)
        return get_index_context(context, PodcastPage, request)

class CourseIndexPage(Page):
    subpage_types = ["CoursePage"]
    parent_page_types = ["HomePage"]
    max_count = 1
    def get_context(self, request):
        context = super().get_context(request)
        return get_index_context(context, CoursePage, request)

class EventPage(Page, ContentMixin):
    content_panels = Page.content_panels + ["title", "preview", "description", "body"]

class NewsPage(Page, ContentMixin):
    content_panels = Page.content_panels + ["title", "preview", "description", "body"]

class PodcastPage(Page, ContentMixin):
    content_panels = Page.content_panels + ["title", "preview", "description", "body"]

class CoursePage(Page, ContentMixin):
    content_panels = Page.content_panels + ["title", "preview", "description", "body"]

def get_index_context(context, page, request):
    allposts = page.objects.live().order_by("-first_published_at")
    paginator = Paginator(allposts, 12)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context["posts"] = posts
    return context