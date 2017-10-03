'''
Created on 24.10.2011

@author: xaralis
'''
from static_sitemaps.views import SitemapView


from django.conf.urls import url


urlpatterns = [
    url(r'^sitemap\.xml$', SitemapView.as_view(), kwargs={'section': 'sitemap'}, name='static_sitemaps_index'),
    url(r'^(?P<section>sitemap-.+)\.xml$',
        SitemapView.as_view()),
]
