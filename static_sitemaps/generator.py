from cStringIO import StringIO
import hashlib
import gzip
import os
import subprocess

from django.contrib.sitemaps import ping_google
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import loader
from django.utils.encoding import smart_str
from django.utils import translation

from static_sitemaps import conf
from static_sitemaps.util import _lazy_load


__author__ = 'xaralis'


class SitemapGenerator(object):
    def __init__(self, verbosity):
        self.verbosity = verbosity
        self.has_changes = False
        self.storage = _lazy_load(conf.STORAGE_CLASS)(location=conf.ROOT_DIR)
        self.sitemaps = _lazy_load(conf.ROOT_SITEMAP)

        if not isinstance(self.sitemaps, dict):
            self.sitemaps = dict(enumerate(self.sitemaps))

    @staticmethod
    def get_hash(bytestream):
        return hashlib.md5(bytestream).digest()

    @staticmethod
    def normalize_url(url):
        if url[-1] != '/':
            url += '/'
        if not url.startswith(('http://', 'https://')):
            if url.startswith('/'):
                from django.contrib.sites.models import Site
                url = 'http://' + Site.objects.get_current().domain + url
            else:
                url = 'http://' + url
        return url

    def _write(self, path, output):
        self.storage.save(path, ContentFile(output))

    def read_hash(self, path):
        with self.storage.open(path) as f:
            result = self.get_hash(f.read())
        return result

    def out(self, string, min_level=1):
        if self.verbosity >= min_level:
            print string

    def write(self):
        self.out('Generating sitemaps.', 1)
        translation.activate(conf.LANGUAGE)
        self.write_index()
        translation.deactivate()
        self.out('Finished generating sitemaps.', 1)

    def write_index(self):
        old_index_md5 = None

        baseurl = self.normalize_url(conf.get_url())
        parts = []

        # Collect all pages and write them.
        for section, site in self.sitemaps.items():
            if callable(site):
                pages = site().paginator.num_pages
            else:
                pages = site.paginator.num_pages

            for page in range(1, pages + 1):
                filename = conf.FILENAME_TEMPLATE % {'section': section,
                                                     'page': page}
                lastmod = self.write_page(site, page, filename)

                if conf.USE_GZIP:
                    filename += '.gz'

                filename = self.storage.url(
                    '%s%s' % (conf.ROOT_DIR, filename)
                )

                parts.append({
                    'location': filename,
                    'lastmod': lastmod
                })

        path = os.path.join(conf.ROOT_DIR, 'sitemap.xml')
        self.out('Writing index file.', 2)

        if self.storage.exists(path):
            old_index_md5 = self.read_hash(path)
            self.storage.delete(path)

        output = loader.render_to_string(conf.INDEX_TEMPLATE, {'sitemaps': parts})
        self._write(path, output)

        with self.storage.open(path) as sitemap_index:
            if self.get_hash(sitemap_index.read()) != old_index_md5:
                self.has_changes = True

        if conf.PING_GOOGLE and self.has_changes:
            try:
                sitemap_url = reverse('static_sitemaps_index')
            except NoReverseMatch:
                sitemap_url = "%ssitemap.xml" % baseurl

            self.out('Pinging google...', 2)
            ping_google(sitemap_url)

    def write_page(self, site, page, filename):
        self.out('Writing sitemap %s.' % filename, 2)
        old_page_md5 = None
        urls = []

        try:
            if callable(site):
                urls.extend(site().get_urls(page))
            else:
                urls.extend(site.get_urls(page))
        except EmptyPage:
            self.out("Page %s empty" % page)
        except PageNotAnInteger:
            self.out("No page '%s'" % page)

        lastmods = [lastmod for lastmod in [u.get('lastmod') for u in urls] if lastmod is not None]
        file_lastmod = max(lastmods) if len(lastmods) > 0 else None
        path = os.path.join(conf.ROOT_DIR, filename)
        template = getattr(site, 'sitemap_template', 'sitemap.xml')

        if self.storage.exists(path):
            old_page_md5 = self.read_hash(path)
            self.storage.delete(path)

        output = smart_str(loader.render_to_string(template, {'urlset': urls}))
        self._write(path, output)

        with self.storage.open(path) as sitemap_page:
            if old_page_md5 != self.get_hash(sitemap_page.read()):
                self.has_changes = True

        if conf.USE_GZIP:
            if conf.GZIP_METHOD not in ['python', 'system', ]:
                raise ImproperlyConfigured("STATICSITEMAPS_GZIP_METHOD must be in ['python', 'system']")

            if conf.GZIP_METHOD == 'system' and not os.path.exists(conf.SYSTEM_GZIP_PATH):
                raise ImproperlyConfigured('STATICSITEMAPS_SYSTEM_GZIP_PATH does not exist')

            if conf.GZIP_METHOD == 'system' and not isinstance(conf.SYSTEM_GZIP_PATH, FileSystemStorage):
                raise ImproperlyConfigured('system gzip method can only be used with FileSystemStorage')

            if conf.GZIP_METHOD == 'system':
                # GZIP with system gzip binary
                subprocess.call([conf.SYSTEM_GZIP_PATH, '-f', path, ])
            else:
                # GZIP with python gzip lib
                try:
                    gzipped_path = '%s.gz' % path
                    if self.storage.exists(gzipped_path):
                        self.storage.delete(gzipped_path)

                    self.out('Compressing...', 2)
                    buf = StringIO()
                    with gzip.GzipFile(fileobj=buf, mode="w") as f:
                        f.write(output)
                    self.storage.save(gzipped_path, ContentFile(buf.getvalue()))
                except OSError:
                    self.out("Compress %s file error" % path)

        return file_lastmod
