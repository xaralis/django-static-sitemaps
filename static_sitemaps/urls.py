from django.urls import path, re_path

from static_sitemaps.views import SitemapView

urlpatterns = [
    path('sitemap.xml', SitemapView.as_view(), kwargs={'section': 'sitemap'}, name='static_sitemaps_index'),
    re_path(r'^(?P<section>sitemap-.+)\.xml$', SitemapView.as_view()),
]
