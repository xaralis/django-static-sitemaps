'''
Created on 24.10.2011

@author: xaralis
'''
import os

from django.conf import settings
from django.conf.urls.defaults import url, patterns
from django.http import HttpResponse

def serve_index(request):
    f = open(os.path.join(settings.STATIC_ROOT, 'sitemap.xml'), 'r')
    content = f.readlines()
    f.close()
    return HttpResponse(content, mimetype='application/xml')

urlpatterns = patterns('',
    url(r'^', serve_index),
)