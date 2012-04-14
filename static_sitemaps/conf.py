'''
Created on 14.4.2012

@author: xaralis
'''
from django.conf import settings

ROOT_SITEMAP = settings.STATICSITEMAPS_ROOT_SITEMAP
ROOT_DIR = getattr(settings, 'STATICSITEMAPS_ROOT_DIR', settings.STATIC_ROOT)
USE_GZIP = getattr(settings, 'STATICSITEMAPS_USE_GZIP', True)
FILENAME_TEMPLATE = getattr(settings,
                            'STATICSITEMAPS_FILENAME_TEMPLATE',
                            'sitemap-%(section)s-%(page)s.xml')
DOMAIN = getattr(settings, 'STATICSITEMAPS_DOMAIN', None)
LANGUAGE = getattr(settings, 'STATICSITEMAPS_LANGUAGE', settings.LANGUAGE_CODE)
PING_GOOGLE = getattr(settings, 'STATICSITEMAPS_PING_GOOGLE', True)
