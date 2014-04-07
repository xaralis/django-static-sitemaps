from cStringIO import StringIO
import hashlib
import gzip
import os
import subprocess

from django.contrib.sitemaps import ping_google
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import loader
from django.utils.encoding import smart_str
from static_sitemaps import conf

from static_sitemaps.util import _lazy_load


__author__ = 'xaralis'


class SitemapGenerator(object):
    def write_index(self):
        old_index_md5 = None
        new_index_md5 = None
        self.has_changes = False

        storage = _lazy_load(conf.STORAGE_CLASS)()
        sitemaps = _lazy_load(conf.ROOT_SITEMAP)

        url = self.normalize_url(conf.URL)
        parts = []

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
                lastmod = self.write_page(site, page, filename, storage)

                if conf.USE_GZIP:
                    filename += '.gz'

                parts.append({
                    'location': '%s%s' % (url, filename),
                    'lastmod': lastmod
                })

        name = os.path.join(conf.ROOT_DIR, 'sitemap.xml')

        if storage.exists(name):
            with storage.open(name) as sitemap_index:
                old_index_md5 = hashlib.md5(sitemap_index.read()).digest()

            storage.delete(name)

        output = loader.render_to_string(conf.INDEX_TEMPLATE, {'sitemaps': parts})
        buf = StringIO()
        buf.write(output)
        buf.seek(0)
        storage.save(name, buf)

        with storage.open(name) as sitemap_index:
            new_index_md5 = hashlib.md5(sitemap_index.read()).digest()

        if old_index_md5 != new_index_md5:
            self.has_changes = True

        if conf.PING_GOOGLE and self.has_changes:
            try:
                sitemap_url = reverse('static_sitemaps_index')
            except NoReverseMatch:
                sitemap_url = "%ssitemap.xml" % url

            ping_google(sitemap_url)

    def normalize_url(self, url):
        if url[-1] != '/':
            url = url + '/'
        if not url.startswith(('http://', 'https://')):
            if url.startswith('/'):
                from django.contrib.sites.models import Site
                url = 'http://' + Site.objects.get_current().domain + url
            else:
                url = 'http://' + url
        return url

    def write_page(self, site, page, filename, storage):
        old_page_md5 = None
        new_page_md5 = None
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

        file_lastmod = urls[0].get('lastmod') if urls else None
        path = os.path.join(conf.ROOT_DIR, filename)
        template = getattr(site, 'sitemap_template', 'sitemap.xml')

        if storage.exists(path):
            with storage.open(path) as sitemap_page:
                old_page_md5 = hashlib.md5(sitemap_page.read()).digest()
            storage.delete(path)

        output = smart_str(loader.render_to_string(template, {'urlset': urls}))
        buf = StringIO()
        buf.write(output)
        buf.seek(0)
        storage.save(path, buf)

        with storage.open(path) as sitemap_page:
            new_page_md5 = hashlib.md5(sitemap_page.read()).digest()

        if old_page_md5 != new_page_md5:
            self.has_changes = True

        if conf.USE_GZIP:
            if conf.GZIP_METHOD not in ['python', 'system', ]:
                raise ImproperlyConfigured("STATICSITEMAPS_GZIP_METHOD must be in ['python', 'system', ]")

            if conf.GZIP_METHOD == 'system' and not os.path.exists(conf.SYSTEM_GZIP_PATH):
                raise ImproperlyConfigured('STATICSITEMAPS_SYSTEM_GZIP_PATH does not exist')

            if conf.GZIP_METHOD == 'system' and not isinstance(conf.SYSTEM_GZIP_PATH, FileSystemStorage):
                raise ImproperlyConfigured('system gzip method can only be used with FileSystemStorage')

            if conf.GZIP_METHOD == 'system':  # gzip with system gzip binary
                subprocess.call([conf.SYSTEM_GZIP_PATH, '-f', path, ])
            else:  # gzip with python gzip lib
                try:
                    gzipped_path = '%s.gz' % path
                    if storage.exists(gzipped_path):
                        storage.delete(gzipped_path)

                    buf = StringIO()
                    with gzip.GzipFile(fileobj=buf, mode="w") as f:
                        f.write(output)
                    storage.save(gzipped_path, buf)
                except OSError:
                    print "Compress %s file error" % path

        return file_lastmod
