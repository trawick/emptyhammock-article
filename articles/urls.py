from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<slug>[^/]+)/$', views.ArticleDetailView.as_view(), name='detail'),
]
