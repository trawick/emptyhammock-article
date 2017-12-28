from django.conf.urls import url

from . import views
from . import autocomplete_views as autocomplete


urlpatterns = [
    url(
        r'^article-autocomplete/$',
        autocomplete.ArticleAutocomplete.as_view(),
        name='article-autocomplete',
    ),
    url(
        r'^page-autocomplete/$',
        autocomplete.PageAutocomplete.as_view(),
        name='page-autocomplete',
    ),
    url(
        r'^search/$',
        views.ArticleSearchResultView.as_view(),
        name='search',
    ),
    url(r'^(?P<slug>[^/]+)/$', views.ArticleDetailView.as_view(), name='detail'),
]
