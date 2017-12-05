from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models
from .admin import ArticleTeaserInRowInlineAdmin


@plugin_pool.register_plugin
class ArticlePlugin(CMSPluginBase):
    model = models.ArticlePluginModel
    render_template = 'articles/plugins/article.html'
    cache = False


@plugin_pool.register_plugin
class SingleArticleTeaserPlugin(CMSPluginBase):
    model = models.SingleArticleTeaserPluginModel
    render_template = 'articles/plugins/single_article_teaser.html'
    cache = False


@plugin_pool.register_plugin
class RowOfArticleTeasersPlugin(CMSPluginBase):
    model = models.RowOfArticleTeasersPluginModel
    render_template = 'articles/plugins/row_of_article_teasers.html'
    inlines = (ArticleTeaserInRowInlineAdmin,)


@plugin_pool.register_plugin
class ArticleFeedPlugin(CMSPluginBase):
    model = models.ArticleFeedPluginModel
    render_template = 'articles/plugins/article_feed.html'
    cache = False


@plugin_pool.register_plugin
class EventFeedPlugin(CMSPluginBase):
    model = models.EventFeedPluginModel
    render_template = 'articles/plugins/article_feed.html'
    cache = False
