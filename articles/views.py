from django.views.generic import DetailView

from .models import Article


class ArticleDetailView(DetailView):
    queryset = Article.objects.filter(visible=True)
