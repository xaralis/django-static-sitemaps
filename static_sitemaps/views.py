import os

from django.http import HttpResponse, Http404
from django.views.generic import View
from django.contrib.sites.requests import RequestSite

from static_sitemaps import conf
from static_sitemaps.util import _lazy_load


class SitemapView(View):
    def get(self, request, *args, **kwargs):
        section = kwargs.get('section')

        site = RequestSite(request)

        try:
            storage = _lazy_load(conf.STORAGE_CLASS)(location=os.path.join(conf.ROOT_DIR, site.domain))
        except TypeError:
            storage = _lazy_load(conf.STORAGE_CLASS)()

        path = os.path.join(conf.ROOT_DIR, site.domain, '{}.xml'.format(section))
        if not storage.exists(path):
            raise Http404('No sitemap file found on %r. Run django-admin.py '
                          'refresh_sitemap first.' % path)

        f = storage.open(path)
        content = f.readlines()
        f.close()
        return HttpResponse(content, content_type='application/xml')
