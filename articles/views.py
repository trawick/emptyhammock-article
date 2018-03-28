from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.views.generic import DetailView, ListView

from .models import Article


class ArticleDetailView(DetailView):
    queryset = Article.objects.filter(visible=True)


class ArticleSearchResultView(ListView):
    model = Article
    template_name = 'articles/article_search_results.html'
    context_object_name = 'articles'
    paginate_by = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_kwargs = {}
        search_settings = getattr(settings, 'ARTICLE_SEARCH_SETTINGS', {})
        if 'config' in search_settings:
            self.config_kwargs['config'] = search_settings['config']

    def get_queryset(self):
        qs = Article.objects.filter(visible=True)

        try:
            search_string = self.request.GET['q']
            qs = qs.annotate(
                search=(
                    SearchVector('title', **self.config_kwargs) +
                    SearchVector('subtitle', **self.config_kwargs) +
                    SearchVector('content', **self.config_kwargs) +
                    SearchVector('location', **self.config_kwargs) +
                    SearchVector('byline', **self.config_kwargs)
                ),
            ).filter(search=SearchQuery(search_string, **self.config_kwargs))
        except KeyError:
            qs = Article.objects.none()

        return qs.order_by('starts_at')
