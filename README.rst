django-static-sitemaps
========================

There are times when your site is too big to serve the ``sitemap.xml`` by your Django application. This little app is meant to help you with such cases. Instead of serving the sitemap.xml from Django, it features a **management command** that generates the ``sitemap.xml`` to the separate files.

Feature highlights:

* Generate sitemap files to your STATIC/MEDIA/(own choice) directory
* Split sitemap files when limit for size is reached
* Gzip the sitemap files when required
* Set different domain for sitemap file
* Ping google that sitemap has changed

Requirements
------------

The only requirement is Django 1.3+. App should work with older Django versions with some settings
tweaks. In matter of fact just defining ``STATICSITEMAPS_ROOT_DIR`` (in case
you have no ``STATIC_ROOT`` defined) should be enough.

Usage
------

Install via standard Python way::

	pip install django-static-sitemaps

Add to you ``INSTALLED_APPS``::

	INSTALLED_APPS = (
		...
		'static_sitemaps',
		...
	)

Set ``STATICSITEMAPS_ROOT_SITEMAP`` variable in your ``settings.py`` to point
to dictionary holding the sitemaps configuration (as seen in Django docs)::

	STATICSITEMAPS_ROOT_SITEMAP = 'myproject.sitemaps.sitemaps'

Include ``static_sitemaps.urls`` to your ``urls.py`` to serve the root
``sitemap.xml`` if you want to serve index file through Django (might be
usefull sometimes when it's hard for you to serve it by webserver itself)::

	urlpatterns = patterns('',
		url(r'^sitemap.xml', include('static_sitemaps.urls')),
	)

Setup your cron to run::

	django-admin.py refresh_sitemap

periodically. Usually, it's enough to set it to run once by 30 minutes or so.

Done.

**Note:** Your sitemap files will be served from ``STATIC_URL`` by default. If your
``STATIC_URL`` is a relative one (e.g. ``/static/``), the result will be
prepended the domain to respect the current ``Site`` object. If your
``STATIC_URL`` is absolute (generally doesn't start with a '/'), sitemaps
URL will respect it completely. If you need more detailed control, see
``STATICSITEMAPS_DOMAIN`` setting.

**Note about sitemap index lastmod:** In the static_sitemaps app the sitemaps 
index works slightly different than the Django's default behaviour. Just like 
Django it also gathers all urls from the generated sitemaps but it also 
includes a new XML tag ``lastmod``. The date/time set in this tag comes 
from the first element of the generated file, so reverse sorting your query 
by your date field will keep this information accurate. This is important to
inform the crawler how fresh is the information inside each sitemap inside the
sitemap_index.xml. 

Advanced settings
------------------

``STATICSITEMAPS_ROOT_DIR``
    Filesystem path to generate the sitemaps files to. Defaults to ``STATIC_ROOT`` directory.

``STATICSITEMAPS_USE_GZIP``
	Defaults to ``True``. If ``True``, gzip compression will be used when generating the sitemaps files (which is very possible by sitemaps specification).

``STATICSITEMAPS_FILENAME_TEMPLATE``
	Template for sitemap parts. Defaults to ``sitemap-%(section)s-%(page)s.xml``.

``STATICSITEMAPS_INDEX_TEMPLATE``
    Template path for sitemap index. Defaults to ``static_sitemaps/sitemap_index.xml``. 

``STATICSITEMAPS_DOMAIN``
	Set this to the domain from which you serve static files in case it it different from domain of your Django application. Defaults to current site's domain.

``STATICSITEMAPS_LANGUAGE``
    Language code to use when generating the sitemaps. Defaults to ``LANGUAGE_CODE`` setting.

``STATICSITEMAPS_PING_GOOGLE``
    Boolean determining whether to ping google after sitemaps have been updated. Defaults to ``True``.


Using a custom template
-----------------------

If you need to use a template different from the Django's default (for example 
to generate a Google News sitemap) you can extend the you Sitemap class and 
setting a ``sitemap_template`` attribute. For Example:

.. sourcecode::

    from django.contrib.sitemaps import GenericSitemap                               
                                                                                 
    class GoogleNewsSitemap(GenericSitemap):                                         
        sitemap_template = 'sitemap_googlenews.xml'


