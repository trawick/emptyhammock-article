import datetime
import math

from cms.models import CMSPlugin, Page
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.functional import lazy
from django.utils.text import slugify
from django.utils.timezone import now
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from taggit.managers import TaggableManager


class Article(models.Model):
    CONTENT = 'content'
    BLOG = 'blog'
    REVIEW = 'review'
    EVENT = 'event'
    VENUE = 'venue'
    PROFILE = 'profile'
    FLAVOR_CHOICES = (
        (CONTENT, 'Generic Content'),
        (BLOG, 'Blog article'),
        (REVIEW, 'Review'),
        (EVENT, 'Event'),
        (VENUE, 'Venue'),
        (PROFILE, 'Profile'),
    )

    visible = models.BooleanField('Is article visible', default=False)
    flavor = models.CharField(max_length=8, choices=FLAVOR_CHOICES, blank=False)
    location = models.CharField(max_length=100, blank=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=80, blank=False)
    slug = models.SlugField(blank=True, max_length=100, unique=True)
    subtitle = models.CharField(max_length=80, blank=True)
    byline = models.CharField(max_length=100, blank=True)
    content = HTMLField(blank=True)

    tags = TaggableManager()

    def clean(self):
        if not self.content and self.flavor != self.EVENT:
            raise ValidationError('This type of article requires content.')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # https://code.djangoproject.com/ticket/12651#comment:14
        _slug = self.slug
        _count = 1
        while True:
            try:
                Article.objects.all().exclude(pk=self.pk).get(slug=_slug)
            except Article.MultipleObjectsReturned:
                pass
            except Article.DoesNotExist:
                break
            _slug = "%s-%s" % (self.slug, _count)
            _count += 1

        self.slug = _slug

        if self.visible:
            if not self.published_at:
                self.published_at = now()
        else:
            self.published_at = None

        if not self.expires_at:
            if self.flavor == self.EVENT and self.starts_at:
                delta = getattr(
                    settings,
                    'ARTICLE_EVENT_EXPIRES_DELTA',
                    datetime.timedelta(hours=6)
                )
                base = self.ends_at or self.starts_at
                self.expires_at = base + delta

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return '{} ({})'.format(
            self.title, self.flavor
        )

    @property
    def article_image(self):
        images = ArticleImage.objects.filter(
            visible=True, article=self
        ).order_by('-primary')
        first = images.first()
        return first.image if first else None


class ArticleTag(models.Model):
    """
    Defines a tag that can be used with an Article (via django-taggit).
    Tags must be predefined using an instance of this model to avoid
    the accidental use of variations in spelling or punctuation.
    """
    name = models.CharField('Tag name', max_length=16, blank=False, unique=True)
    meaning = models.CharField('Meaning', max_length=80, blank=True)

    def __str__(self):
        if self.meaning:
            return '{} ({})'.format(self.name, self.meaning)
        else:
            return self.name


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, null=False, blank=False)
    visible = models.BooleanField('Is image visible', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    primary = models.BooleanField(default=False)
    image = FilerImageField(null=False, blank=False)


class ArticleRelatedArticle(models.Model):
    article = models.ForeignKey(Article, null=False, blank=False)
    other_article = models.ForeignKey(
        Article, null=False, blank=False, related_name='related_article'
    )
    override_title = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return 'Reference from {} to {}'.format(self.article, self.other_article)

    @property
    def title(self):
        return self.override_title or self.other_article.title

    class Meta(object):
        verbose_name = 'Other article related to this article'
        verbose_name_plural = 'Other articles related to this article'


class ArticleRelatedPage(models.Model):
    article = models.ForeignKey(Article, null=False, blank=False)
    page = models.ForeignKey(Page, null=True, blank=False, on_delete=models.SET_NULL)
    override_title = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return 'Reference from {} to {}'.format(self.article, self.page)

    @property
    def title(self):
        return self.override_title or self.page.title_set.first().title

    class Meta(object):
        verbose_name = 'Page related to this article'
        verbose_name_plural = 'Pages related to this article'


class ArticleRelatedURL(models.Model):
    article = models.ForeignKey(Article, null=False, blank=False)
    url = models.URLField(blank=False)
    title = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return 'Reference from {} to {}'.format(self.article, self.url)

    class Meta(object):
        verbose_name = 'URL related to this article'
        verbose_name_plural = 'URLs related to this article'


class ArticlePluginModel(CMSPlugin):
    article = models.ForeignKey(Article)

    def __str__(self):
        return str(self.article)


class ArticleTeaserData(CMSPlugin):
    article = models.ForeignKey(Article, null=False, blank=False)
    override_title = models.CharField(max_length=80, blank=True)
    override_subtitle = models.CharField(max_length=80, blank=True)
    override_content = HTMLField(blank=True)
    override_image = FilerImageField(null=True, blank=True)

    def __str__(self):
        return str(self.article)

    @property
    def title(self):
        return self.override_title or self.article.title

    @property
    def subtitle(self):
        return self.override_subtitle or self.article.subtitle

    @property
    def content(self):
        return self.override_content or self.article.content

    @property
    def image(self):
        return self.override_image or self.article.article_image

    class Meta(object):
        abstract = True


class SingleArticleTeaserPluginModel(CMSPlugin):
    ACTION = 'action'
    LINK = 'link'
    SIMPLE = 'simple'
    FLAVOR_CHOICES = (
        (ACTION, 'Bold headings and action button'),
        (LINK, 'Photo and read-more button'),
        (SIMPLE, 'Simple')
    )
    article = models.ForeignKey(Article, null=False, blank=False)
    flavor = models.CharField(max_length=8, choices=FLAVOR_CHOICES, blank=False)
    override_title = models.CharField(max_length=80, blank=True)
    override_subtitle = models.CharField(max_length=80, blank=True)
    override_content = HTMLField(blank=True)
    override_image = FilerImageField(null=True, blank=True)

    def __str__(self):
        return str(self.article)

    @property
    def title(self):
        return self.override_title or self.article.title

    @property
    def subtitle(self):
        return self.override_subtitle or self.article.subtitle

    @property
    def image(self):
        return self.override_image or self.article.article_image


class RowOfArticleTeasersPluginModel(CMSPlugin):

    def copy_relations(self, old_instance):
        self.articleteaserinrow_set.all().delete()
        for article in old_instance.articleteaserinrow_set.all():
            article.pk = None
            article.row = self
            article.save()

    def __str__(self):
        return ','.join([
            str(article)
            for article in self.articleteaserinrow_set.all()
        ])

    @property
    def columns_per_12_grid(self):
        count = self.articleteaserinrow_set.count()
        return math.floor(12 / (count or 12))


class ArticleTeaserInRow(ArticleTeaserData):
    row = models.ForeignKey(RowOfArticleTeasersPluginModel, null=False, blank=False)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ('order',)
        unique_together = ('row', 'order')


def _get_choices(plugin_nickname):
    choices = settings.ARTICLE_PLUGIN_SETTINGS[plugin_nickname]['choices']
    return [
        (choice['flavor'], choice['description'])
        for choice in choices
    ]


def get_feed_choices():
    return _get_choices('ArticleFeed')


class BaseFeedPluginModel(CMSPlugin):
    flavor = models.PositiveSmallIntegerField(blank=False, default=1, choices=lazy(get_feed_choices, list)())
    tags = models.ManyToManyField(ArticleTag, blank=True)
    override_nothing_found = models.CharField(
        'Use this text instead of "Nothing found"', max_length=120, blank=True
    )

    def filter_by_tags(self, qs):
        tags = [x.name for x in self.tags.all()]
        if tags:
            qs = qs.filter(tags__name__in=tags).distinct()
        return qs

    def copy_relations(self, old_instance):
        self.tags.clear()
        for tag in old_instance.tags.all():
            self.tags.add(tag)

    class Meta:
        abstract = True


class ArticleFeedPluginModel(BaseFeedPluginModel):
    title = models.CharField(max_length=40, blank=False)
    max_articles = models.SmallIntegerField(default=6)
    include_content = models.BooleanField(default=False)
    include_blog = models.BooleanField(default=False)
    include_review = models.BooleanField(default=False)
    include_event = models.BooleanField(default=False)
    include_venue = models.BooleanField(default=False)
    include_profile = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def articles(self):
        flavors = []
        if self.include_content:
            flavors.append(Article.CONTENT)
        if self.include_blog:
            flavors.append(Article.BLOG)
        if self.include_review:
            flavors.append(Article.REVIEW)
        if self.include_event:
            flavors.append(Article.EVENT)
        if self.include_venue:
            flavors.append(Article.VENUE)
        if self.include_profile:
            flavors.append(Article.PROFILE)
        qs = Article.objects.filter(
            visible=True,
            flavor__in=flavors
        )
        qs = self.filter_by_tags(qs)
        return qs.order_by('-modified_at')[:self.max_articles]


class EventFeedPluginModel(BaseFeedPluginModel):
    title = models.CharField(max_length=40, blank=False)
    max_articles = models.SmallIntegerField(default=6)
    max_days_ahead = models.SmallIntegerField(default=30)

    def __str__(self):
        return self.title

    @property
    def articles(self):
        right_now = now()
        earlier_today = right_now.replace(hour=max(0, right_now.hour - 4))
        cutoff = right_now + datetime.timedelta(days=self.max_days_ahead)
        qs = Article.objects.filter(
            visible=True,
            flavor=Article.EVENT,
            starts_at__gte=earlier_today,
        )
        qs = qs.filter(Q(ends_at__isnull=True) | Q(ends_at__lte=cutoff))
        qs = self.filter_by_tags(qs)
        return qs.order_by('starts_at')[:self.max_articles]
