from django.conf import settings

try:
    from celery.schedules import crontab
except ImportError:
    crontab = None


# Base sitemap config dict as stated in Django docs.
ROOT_SITEMAP = settings.STATICSITEMAPS_ROOT_SITEMAP

# Path to root location where the sitemaps will be stored.
ROOT_DIR = getattr(settings, 'STATICSITEMAPS_ROOT_DIR', settings.STATIC_ROOT)

# Compress the result?
USE_GZIP = getattr(settings, 'STATICSITEMAPS_USE_GZIP', True)

# How to compress it? Must be in ('python', 'system').
GZIP_METHOD = getattr(settings, 'STATICSITEMAPS_GZIP_METHOD', 'python')

# Path to system gzip binary if system method is selected.
SYSTEM_GZIP_PATH = getattr(settings, 'STATICSITEMAPS_SYSTEM_GZIP_PATH', '/usr/bin/gzip')

# Template how to name the resulting sitemap pages.
FILENAME_TEMPLATE = getattr(settings,
                            'STATICSITEMAPS_FILENAME_TEMPLATE',
                            'sitemap-%(section)s-%(page)s.xml')

# Only for backwards compatibility, same as URL.
DOMAIN = getattr(settings, 'STATICSITEMAPS_DOMAIN', None)

# Language of sitemaps.
LANGUAGE = getattr(settings, 'STATICSITEMAPS_LANGUAGE', settings.LANGUAGE_CODE)

# Ping google after something changed in sitemap?
PING_GOOGLE = getattr(settings, 'STATICSITEMAPS_PING_GOOGLE', True)

# Template for sitemap index.
INDEX_TEMPLATE = getattr(settings, 'STATICSITEMAPS_INDEX_TEMPLATE',
                         'static_sitemaps/sitemap_index.xml')

# Storage class to use.
STORAGE_CLASS = getattr(settings, 'STATICSITEMAPS_STORAGE', 'django.core.files.storage.FileSystemStorage')

# When should the celery task be run.
CELERY_TASK_SCHEDULE = getattr(
    settings, 'STATICSITEMAPS_REFRESH_ON', crontab(minute=0) if crontab else None)

# URL to serve sitemaps from.
_url = getattr(settings, 'STATICSITEMAPS_URL', None)

# Force the protocol to use with django sites framework
FORCE_PROTOCOL = getattr(settings, 'STATICSITEMAPS_FORCE_PROTOCOL', None)

# Mock django sites framework
MOCK_SITE = getattr(settings, 'STATICSITEMAPS_MOCK_SITE', False)

# Mock django sites framework with hostname string...for example www.yoursite.com
MOCK_SITE_NAME = getattr(settings, 'STATICSITEMAPS_MOCK_SITE_NAME', None)

# Mock django sites framework with https | https
MOCK_SITE_PROTOCOL = getattr(settings, 'STATICSITEMAPS_MOCK_SITE_PROTOCOL', 'http')


def get_url(site):
    _url = getattr(settings, 'STATICSITEMAPS_URL', None)
    if _url is not None:
        return _url + site.domain + '/'

    if DOMAIN:
        # Backwards compatibility.
        import warnings
        _url = DOMAIN
        warnings.warn('You are using STATICSITEMAPS_DOMAIN which is going to be '
                      'deprecated soon. Please migrate to '
                      'STATICSITEMAPS_URL', DeprecationWarning)
    elif settings.STATIC_URL.startswith('/'):
        # If STATIC_URL starts with '/', it is probably a relative URL to the
        # current domain so we append STATIC_URL.
        _url = site.domain + settings.STATIC_URL + site.domain + '/'
    else:
        # If STATIC_URL starts with protocol, it is probably a special domain
        # for static files and we stick to it.
        _url = settings.STATIC_URL
    return _url
