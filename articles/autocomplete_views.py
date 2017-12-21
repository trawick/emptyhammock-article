from cms.models import Page
from dal import autocomplete

from .models import Article


class ArticleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_staff:
            return Article.objects.none()

        qs = Article.objects.filter(visible=True)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        # must be ordered to avoid a Django inconsistent-pagination warning
        return qs.order_by('title')


class PageAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return Page.objects.none()

        qs = Page.objects.drafts()
        if self.q:
            qs = qs.filter(title_set__title__icontains=self.q)

        return qs
