import logging

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import ArticleImportForm

logger = logging.getLogger(__name__)


class ImportEventsView(FormView):
    template_name = 'articles/admin/import_events.html'
    form_class = ArticleImportForm

    def get_success_url(self):
        app_label, object_name = 'articles', 'article'
        return reverse('admin:%s_%s_changelist' % (app_label, object_name))

    def form_valid(self, form):
        form.import_events()
        return super().form_valid(form)
