django-static-sitemaps
========================

There are times when your site is too big to serve the ``sitemap.xml`` by your Django application. This little app is meant to help you with such cases. Instead of serving the sitemap.xml from Django, it features a **management command**/**celery task** that generates the ``sitemap.xml`` to the separate files.

Feature highlights:

* **NEW:** Compatible with Django 2.0+
* **NEW:** Python 3 compatible
* Generate sitemap files to your STATIC/MEDIA/(own choice) directory
* Split sitemap files when limit for size is reached
* gzip the sitemap files when required
* Set different domain for sitemap file
* Ping google that sitemap has changed

Python 2 users
------

Python 2 users have should use `4.4.0`. Newer versions will by Python 3 compatible only. Sorry about that.

Requirements
------------

The only requirement is Django 1.8+. App should work with older Django versions with some settings
tweaks.


Usage
------

Install via standard Python way::

	pip install django-static-sitemaps

Add `static_sitemaps` to you ``INSTALLED_APPS`` and make sure
`django.contrib.sitemaps` is present too:

```python
INSTALLED_APPS = (
    ...
    'django.contrib.sites',
    'django.contrib.sitemaps',
    ...
    'static_sitemaps',
    ...
)

SITE_ID = 1
```

Remember to run `python manage.py makemigrations` and `python manage.py migrate`.

Set ``STATICSITEMAPS_ROOT_SITEMAP`` variable in your ``settings.py`` to point
to dictionary holding the sitemaps configuration (as seen in Django docs)::

	STATICSITEMAPS_ROOT_SITEMAP = 'myproject.sitemaps.sitemaps'

Also, make sure you have `STATICSITEMAPS_ROOT_DIR` or at least `STATIC_ROOT` configured.
Sitemap files will be placed there.

Include ``static_sitemaps.urls`` to your ``urls.py`` to serve the root
``sitemap.xml`` if you want to serve index file through Django (might be
usefull sometimes when it's hard for you to serve it by webserver itself):

	urlpatterns = [
	    path('', include('static_sitemaps.urls')),
	]

Setup your cron to run::

	django-admin.py refresh_sitemap

periodically. Usually, it's enough to set it to run once by 30 minutes or so.

For Windows users you can alternatively use the following command:

	python manage.py runserver

Done.

Alternatively, you can run this using a Celery task runner. For details, look below.

**Note:** Your sitemap files will be served from ``STATIC_URL`` by default. If your
``STATIC_URL`` is a relative one (e.g. ``/static/``), the result will be
prepended the domain to respect the current ``Site`` object. If your
``STATIC_URL`` is absolute (generally doesn't start with a '/'), sitemaps
URL will respect it completely. If you need more detailed control, see
``STATICSITEMAPS_URL`` setting.

**Note about sitemap index lastmod:** In the static_sitemaps app the sitemaps
index works slightly different than the Django's default behaviour. Just like
Django it also gathers all urls from the generated sitemaps but it also
includes a new XML tag ``lastmod``. The date/time set in this tag comes
from the first element of the generated file, so reverse sorting your query
by your date field will keep this information accurate. This is important to
inform the crawler how fresh is the information inside each sitemap inside the
sitemap_index.xml.

Running as celery task
----------------------

If you run celery as your task runner, you should be ready to go out of the box. django-static-sitemaps includes the ``GenerateSitemap`` task which will be automatically run each ``STATICSITEMAPS_REFRESH_AFTER`` minutes (defaults to 60 ~ 1 hour). You can optionally bypass it by setting it to ``None``.

Advanced settings
------------------

``STATICSITEMAPS_ROOT_DIR``
    Filesystem path to generate the sitemaps files to. Defaults to ``STATIC_ROOT`` directory.

``STATICSITEMAPS_USE_GZIP``
	Defaults to ``True``. If ``True``, gzip compression will be used when generating the sitemaps files (which is very possible by sitemaps specification).

``STATICSITEMAPS_GZIP_METHOD``
    Gzip method to use. Must be in ['python', 'system', ].

``STATICSITEMAPS_SYSTEM_GZIP_PATH``
    Path to the gzip binary if use STATICSITEMAPS_GZIP_METHOD == 'system'.

``STATICSITEMAPS_FILENAME_TEMPLATE``
	Template for sitemap parts. Defaults to ``sitemap-%(section)s-%(page)s.xml``.

``STATICSITEMAPS_INDEX_TEMPLATE``
    Template path for sitemap index. Defaults to ``static_sitemaps/sitemap_index.xml``.

``STATICSITEMAPS_URL``
	Set this to the URL from which you want to serve the sitemaps. Can be an URL with and without domain, e.g. http://example.com/media/sitemaps/ or /media/sitemaps/.
	If no domain is given, the domain of the current Django site is used. Default is STATIC_URL.

``STATICSITEMAPS_LANGUAGE``
    Language code to use when generating the sitemaps. Defaults to ``LANGUAGE_CODE`` setting.

``STATICSITEMAPS_PING_GOOGLE``
    Boolean determining whether to ping google after sitemaps have been updated. Defaults to ``True``. Please note that google will only be notified if something changed in the sitemap file set.

``STATICSITEMAPS_REFRESH_AFTER``
    How often (in minutes) should the celery task be run. Defaults to 60 minutes.

``STATICSITEMAPS_MOCK_SITE``
    True|False setting if you want to mock the Django sites framework. Useful if you want to use package without enabling django.contrib.sites. Defaults to False.

``STATICSITEMAPS_MOCK_SITE_NAME``
    URL of the site your mocking. This is what will show up in your sitemap as the URL. For example: 'www.yoursite.com'. Defaults to None.

``STATICSITEMAPS_MOCK_SITE_PROTOCOL``
    Protocol to use when mocking above site name. Defaults to 'http'.

``STATICSITEMAPS_STORAGE``
    Storage class to use. Defaults to ``django.core.files.storage.FileSystemStorage``.


Using a custom template
-----------------------

If you need to use a template different from the Django's default (for example
to generate a Google News sitemap) you can extend the you Sitemap class and
setting a ``sitemap_template`` attribute. For example:

    from django.contrib.sitemaps import GenericSitemap

    class GoogleNewsSitemap(GenericSitemap):
        sitemap_template = 'sitemap_googlenews.xml'
