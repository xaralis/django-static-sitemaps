from static_sitemaps.views import SitemapView

try:
    from django.urls import path, re_path

    urlpatterns = [
        path('sitemap.xml', SitemapView.as_view(), kwargs={'section': 'sitemap'}, name='static_sitemaps_index'),
        re_path(r'^(?P<section>sitemap-.+)\.xml$', SitemapView.as_view()),
    ]
except ImportError: # Django < 2.0
    from django.conf.urls import url

    urlpatterns = [
        url(r'^sitemap\.xml$', SitemapView.as_view(), kwargs={'section': 'sitemap'}, name='static_sitemaps_index'),
        url(r'^(?P<section>sitemap-.+)\.xml$', SitemapView.as_view()),
    ]
