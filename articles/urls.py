from django.urls import path

from . import views
from . import autocomplete_views as autocomplete

app_name = 'articles'

urlpatterns = [
    path(
        'article-autocomplete/',
        autocomplete.ArticleAutocomplete.as_view(),
        name='article-autocomplete',
    ),
    path(
        'page-autocomplete/',
        autocomplete.PageAutocomplete.as_view(),
        name='page-autocomplete',
    ),
    path(
        'search/',
        views.ArticleSearchResultView.as_view(),
        name='search',
    ),
    path(
        'view/<str:slug>/',
        views.ArticleDetailView.as_view(),
        name='detail'
    ),
]
