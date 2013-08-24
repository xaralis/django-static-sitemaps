'''
Created on 14.4.2012

@author: xaralis
'''

from django.conf import settings

ROOT_SITEMAP = settings.STATICSITEMAPS_ROOT_SITEMAP
ROOT_DIR = getattr(settings, 'STATICSITEMAPS_ROOT_DIR', settings.STATIC_ROOT)
USE_GZIP = getattr(settings, 'STATICSITEMAPS_USE_GZIP', True)
GZIP_METHOD = getattr(settings, 'STATICSITEMAPS_GZIP_METHOD', 'python')  # must be in ['python', 'system', ]
SYSTEM_GZIP_PATH = getattr(settings, 'STATICSITEMAPS_SYSTEM_GZIP_PATH', '/usr/bin/gzip')
FILENAME_TEMPLATE = getattr(settings,
                            'STATICSITEMAPS_FILENAME_TEMPLATE',
                            'sitemap-%(section)s-%(page)s.xml')
URL = getattr(settings, 'STATICSITEMAPS_URL', None)
DOMAIN = getattr(settings, 'STATICSITEMAPS_DOMAIN', None)
LANGUAGE = getattr(settings, 'STATICSITEMAPS_LANGUAGE', settings.LANGUAGE_CODE)
PING_GOOGLE = getattr(settings, 'STATICSITEMAPS_PING_GOOGLE', True)
INDEX_TEMPLATE = getattr(settings, 'STATICSITEMAPS_INDEX_TEMPLATE',
                         'static_sitemaps/sitemap_index.xml')

CELERY_TASK_REPETITION = getattr(settings, 'STATICSITEMAPS_REFRESH_AFTER', 60 * 60)


if URL is None:
    if DOMAIN: # backward compatibility
        URL = DOMAIN
    elif settings.STATIC_URL.startswith('/'):
        # If STATIC_URL starts with '/', it is probably a relative URL to the
        # current domain so we append STATIC_URL.
        from django.contrib.sites.models import Site
        URL = Site.objects.get_current().domain + settings.STATIC_URL
    else:
        # If STATIC_URL starts with protocol, it is probably a special domain
        # for static files and we stick to it.
        URL = settings.STATIC_URL
