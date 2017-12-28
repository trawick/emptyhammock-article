from django.contrib.postgres.search import SearchVector
from django.views.generic import DetailView, ListView

from .models import Article


class ArticleDetailView(DetailView):
    queryset = Article.objects.filter(visible=True)


class ArticleSearchResultView(ListView):
    model = Article
    template_name = 'articles/article_search_results.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        qs = Article.objects.filter(visible=True)

        try:
            search_string = self.request.GET['q']
            qs = qs.annotate(
                search=(
                    SearchVector('title') +
                    SearchVector('content') +
                    SearchVector('location') +
                    SearchVector('byline')
                ),
            ).filter(search=search_string)
        except KeyError:
            return Article.objects.none()

        return qs.order_by('starts_at')
