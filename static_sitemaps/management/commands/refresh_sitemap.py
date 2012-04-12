'''
Created on 21.10.2011

@author: xaralis
'''
import os, subprocess

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sitemaps import ping_google
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.management.base import NoArgsCommand
from django.template import loader
from django.utils import translation
from django.utils.encoding import smart_str
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

STATICSITEMAPS_USE_GZIP = getattr(settings, 'STATICSITEMAPS_ROOT_SITEMAP', True)
STATICSITEMAPS_FILENAME_TEMPLATE = getattr(settings, 'STATICSITEMAPS_FILENAME_TEMPLATE', 'sitemap-%(section)s-%(page)s.xml')
STATICSITEMAPS_SITEMAP_DOMAIN = getattr(settings, 'STATICSITEMAPS_SITEMAP_DOMAIN', None)
STATICSITEMAPS_ROOT_SITEMAP = settings.STATICSITEMAPS_ROOT_SITEMAP

class Command(NoArgsCommand):
    command = None
    
    def write_index(self):
        module, attr = STATICSITEMAPS_ROOT_SITEMAP.rsplit('.', 1)
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

        domain = STATICSITEMAPS_SITEMAP_DOMAIN or Site.objects.get_current().domain
        sites = []
        
        for section, site in sitemaps.items():
            if callable(site):
                pages = site().paginator.num_pages
            else:
                pages = site.paginator.num_pages
                
            for page in range(1, pages + 1):
                filename = STATICSITEMAPS_FILENAME_TEMPLATE % {'section': section, 'page': page}
                self.write_page(site, page, filename)
                
                if STATICSITEMAPS_USE_GZIP:
                    filename += '.gz'
                
                if domain[-1] == '/':
                    sites.append('%s%s' % (domain, filename))
                else:
                    sites.append('%s/%s' % (domain, filename))
        f = open(os.path.join(settings.STATIC_ROOT, 'sitemap.xml'), 'w')
        f.write(smart_str(loader.render_to_string('sitemap_index.xml', {'sitemaps': sites})))
        f.close()
        ping_google('sitemap.xml')
    
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
           
        path = os.path.join(settings.STATIC_ROOT, filename)
            
        if os.path.exists(path):
            os.unlink(path)
            
        f = open(path, 'w')
        f.write(smart_str(loader.render_to_string('sitemap.xml', {'urlset': urls})))
        f.close()
        
        if STATICSITEMAPS_USE_GZIP:
            subprocess.call(['gzip', '-f', os.path.join(settings.STATIC_ROOT, filename)])

    def handle_noargs(self, **options):
        translation.activate(settings.LANGUAGE_CODE)
        self.write_index()
        translation.deactivate()
            
