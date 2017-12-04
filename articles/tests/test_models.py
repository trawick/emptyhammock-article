from django.test import TestCase

from apps.articles.models import Article


class TestArticle(TestCase):

    def test_slug_uniqueness(self):
        article = Article(title='foo', flavor=Article.EVENT)
        article.full_clean()
        article.save()
        slug1 = article.slug

        article = Article(title='foo', flavor=Article.EVENT)
        article.full_clean()
        article.save()
        slug2 = article.slug

        self.assertNotEqual(slug1, slug2)
