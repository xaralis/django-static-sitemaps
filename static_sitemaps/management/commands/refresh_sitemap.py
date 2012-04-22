'''
Created on 21.10.2011

@author: xaralis
'''
import os
import subprocess

from django.contrib.sitemaps import ping_google
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.management.base import NoArgsCommand
from django.core.urlresolvers import reverse
from django.template import loader
from django.utils import translation
from django.utils.encoding import smart_str
from django.utils.importlib import import_module

from static_sitemaps import conf


class Command(NoArgsCommand):
    command = None
    help = 'Generates sitemaps files to a predefined directory.'

    def write_index(self):
        module, attr = conf.ROOT_SITEMAP.rsplit('.', 1)
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                       (module, e))
        try:
            sitemaps = getattr(mod, attr)
        except AttributeError:
            raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                       'class.' % (module, attr))

        domain = self.normalize_domain(conf.DOMAIN)
        sites = []

        if not isinstance(sitemaps, dict):
            sitemaps = dict(enumerate(sitemaps))

        for section, site in sitemaps.items():
            if callable(site):
                pages = site().paginator.num_pages
            else:
                pages = site.paginator.num_pages

            for page in range(1, pages + 1):
                filename = conf.FILENAME_TEMPLATE % {'section': section,
                                                     'page': page}
                self.write_page(site, page, filename)

                if conf.USE_GZIP:
                    filename += '.gz'

                sites.append('%s%s' % (domain, filename))
        f = open(os.path.join(conf.ROOT_DIR, 'sitemap.xml'), 'w')
        f.write(smart_str(loader.render_to_string('sitemap_index.xml',
                                                  {'sitemaps': sites})))
        f.close()

        if conf.PING_GOOGLE:
            ping_google(reverse('static_sitemaps_index'))

    def normalize_domain(self, domain):
        if domain[-1] != '/':
            domain = domain + '/'
        if not domain.startswith(('http://', 'https://')):
            domain = 'http://' + domain
        return domain

    def write_page(self, site, page, filename):
        urls = []
        try:
            if callable(site):
                urls.extend(site().get_urls(page))
            else:
                urls.extend(site.get_urls(page))
        except EmptyPage:
            print "Page %s empty" % page
        except PageNotAnInteger:
            print "No page '%s'" % page

        path = os.path.join(conf.ROOT_DIR, filename)

        if os.path.exists(path):
            os.unlink(path)

        f = open(path, 'w')
        f.write(smart_str(loader.render_to_string('sitemap.xml',
                                                  {'urlset': urls})))
        f.close()

        if conf.USE_GZIP:
            subprocess.call(['gzip', '-f', os.path.join(conf.ROOT_DIR,
                                                        filename)])

    def handle_noargs(self, **options):
        translation.activate(conf.LANGUAGE)
        self.write_index()
        translation.deactivate()
