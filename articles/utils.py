import logging

from django.utils.timezone import now

from .models import Article

logger = logging.getLogger(__name__)


def expire_articles():
    """
    This should be called periodically to ensure that articles which have
    expired are not visible.
    """
    cutoff = now()
    updated = Article.objects.filter(
        visible=True, expires_at__lte=cutoff
    ).update(visible=False)
    logger.info('%s articles were expired at %s', updated, cutoff)
