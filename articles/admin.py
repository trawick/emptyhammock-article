from django.urls import path
from django.contrib import admin
from django.db import models
from django import forms
from taggit.models import TaggedItem

from .admin_views import ImportEventsView
from .forms import (
    ArticleAdminForm, ArticleRelatedArticleAdminForm,
    ArticleRelatedPageAdminForm, ArticleTeaserInRowAdminForm
)
from .models import (
    Article, ArticleImage, ArticleRelatedArticle, ArticleRelatedPage,
    ArticleRelatedURL, ArticleTag, ArticleTeaserInRow
)


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 0


class FixCharFieldsMixin(object):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '80'})},
        models.URLField: {'widget': forms.TextInput(attrs={'size': '80'})},
    }


class ArticleRelatedArticleInline(FixCharFieldsMixin, admin.StackedInline):
    model = ArticleRelatedArticle
    fk_name = 'article'
    extra = 0
    form = ArticleRelatedArticleAdminForm


class ArticleRelatedPageInline(FixCharFieldsMixin, admin.StackedInline):
    model = ArticleRelatedPage
    form = ArticleRelatedPageAdminForm
    extra = 0


class ArticleRelatedURLInline(FixCharFieldsMixin, admin.StackedInline):
    model = ArticleRelatedURL
    extra = 0


@admin.action(
    description='Duplicate selected articles'
)
def duplicate_articles(modeladmin, request, queryset):
    # The duplicate copy will be like the original, even with associated
    # data duplicated, except that:
    # - The title will have " (copy)" appended
    # - The duplicate won't be visible on the site
    # - The duplicate will have creator_key cleared (e.g., so the duplicate
    #   wouldn't be wiped out by some workflows that use that field, thinking
    #   that the duplicate was created by that workflow).
    # - The slug will be unique.
    for obj in queryset:
        orig_pk = obj.pk
        new_article = obj
        new_article.pk = None
        new_article.title = '{} (copy)'.format(new_article.title)
        new_article.creator_key = ''
        new_article.visible = False
        # The slug is taken care of in .save()
        new_article.save()

        orig_article = Article.objects.get(pk=orig_pk)
        # Copy tags
        for tag in orig_article.tags.all():
            TaggedItem.objects.create(content_object=new_article, tag=tag)

        # Copy images, related articles, related pages, related URLs
        for set_to_copy in (
            orig_article.articleimage_set,
            orig_article.articlerelatedarticle_set,
            orig_article.articlerelatedarticle_set,
            orig_article.articlerelatedurl_set
        ):
            for related in set_to_copy.all():
                related.pk = None
                related.article = new_article
                related.save()


@admin.action(
    description='Hide selected articles'
)
def hide_articles(modeladmin, request, queryset):
    queryset.update(visible=False)


@admin.action(
    description='Show selected articles'
)
def show_articles(modeladmin, request, queryset):
    queryset.update(visible=True)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = [duplicate_articles, hide_articles, show_articles]
    change_list_template = 'articles/admin/article_change_list.html'
    form = ArticleAdminForm
    inlines = (
        ArticleImageInline, ArticleRelatedArticleInline,
        ArticleRelatedPageInline, ArticleRelatedURLInline,
    )
    list_display = ('title', 'visible', 'flavor', 'starts_at', 'modified_at', )
    list_filter = ('visible', 'flavor', 'creator_key', )
    readonly_fields = ('created_at', 'published_at', 'modified_at', )
    search_fields = ('title', 'content', 'subtitle', 'location', 'byline', )
    fieldsets = (
        (None, {
            'fields': (
                'visible', 'flavor', 'title', 'subtitle', 'byline', 'content',
                'tags',
            )
        }),
        ('Event-specific fields', {
            'fields': (
                'location', 'starts_at', 'ends_at',
            )
        }),
        ('Other fields', {
            'classes': ('collapse', ),
            'fields': (
                'expires_at', 'slug', 'creator_key',
                'created_at', 'modified_at', 'published_at',
            )
        })
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                'import_events/', ImportEventsView.as_view(),
                name='%s_%s_import_events' % (
                    self.model._meta.app_label, self.model._meta.model_name
                )
            ),
        ]
        return my_urls + urls


admin.site.register(ArticleTag)


class ArticleTeaserInRowInlineAdmin(admin.StackedInline):
    model = ArticleTeaserInRow
    fk_name = 'row'
    form = ArticleTeaserInRowAdminForm
