'''
Created on 24.10.2011

@author: xaralis
'''
import os

from django.http import HttpResponse, Http404

from static_sitemaps import conf
from static_sitemaps.util import _lazy_load


try:
    from django.conf.urls import url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, url


def serve_index(request):
    storage = _lazy_load(conf.STORAGE_CLASS)(location=conf.ROOT_DIR)
    path = os.path.join(conf.ROOT_DIR, 'sitemap.xml')
    if not storage.exists(path):
        raise Http404('No sitemap index file found on %r. Run django-admin.py '
                      'refresh_sitemap first.' % path)

    f = storage.open(path)
    content = f.readlines()
    f.close()
    return HttpResponse(content, content_type='application/xml')

urlpatterns = [
    url(r'^', serve_index, name='static_sitemaps_index'),
]
