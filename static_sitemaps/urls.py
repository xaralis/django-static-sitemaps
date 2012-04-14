'''
Created on 24.10.2011

@author: xaralis
'''
import os

from django.conf.urls.defaults import url, patterns
from django.http import HttpResponse, Http404

from static_sitemaps import conf


def serve_index(request):
    path = os.path.join(conf.ROOT_DIR, 'sitemap.xml')
    if not os.path.exists(path):
        raise Http404('No sitemap index file found on %r. Run django-admin.py '
                      'refresh_sitemap first.' % path)
    f = open(path)
    content = f.readlines()
    f.close()
    return HttpResponse(content, mimetype='application/xml')

urlpatterns = patterns('',
    url(r'^', serve_index, name='static_sitemaps_index'),
)
