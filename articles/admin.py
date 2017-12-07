from cms.models import Page
from django.conf.urls import url
from django.contrib import admin
from django.db import models
from django import forms

from .admin_views import ImportEventsView
from .forms import ArticleAdminForm
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


class ArticleRelatedPageAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['page'].queryset = Page.objects.drafts()


class ArticleRelatedPageInline(FixCharFieldsMixin, admin.StackedInline):
    model = ArticleRelatedPage
    form = ArticleRelatedPageAdminForm
    extra = 0


class ArticleRelatedURLInline(FixCharFieldsMixin, admin.StackedInline):
    model = ArticleRelatedURL
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    change_list_template = 'articles/admin/article_change_list.html'
    form = ArticleAdminForm
    inlines = (
        ArticleImageInline, ArticleRelatedArticleInline,
        ArticleRelatedPageInline, ArticleRelatedURLInline,
    )
    list_display = ('title', 'flavor', 'starts_at', 'modified_at', 'expires_at', )
    list_filter = ('visible', 'flavor', )
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
                'expires_at',
                'slug', 'created_at', 'modified_at', 'published_at',
            )
        })
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(
                r'^import_events/$', ImportEventsView.as_view(),
                name='%s_%s_import_events' % (
                    self.model._meta.app_label, self.model._meta.model_name
                )
            ),
        ]
        return my_urls + urls


admin.site.register(Article, ArticleAdmin)

admin.site.register(ArticleTag)


class ArticleTeaserInRowInlineAdmin(admin.StackedInline):
    model = ArticleTeaserInRow
    fk_name = 'row'
