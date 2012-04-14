django-static-sitemaps
========================

There are times when your site is too big to serve the ``sitemap.xml`` by your Django application. This little app is meant to help you with such cases. Instead of serving the sitemap.xml from Django, it features a **management command** that generates the ``sitemap.xml`` to the separate files.

Feature highlights:

* Generate sitemap files to your STATIC/MEDIA/(own choice) directory
* Split sitemap files when limit for size is reached 
* Gzip the sitemap files when required
* Set different domain for sitemap file
* Ping google that sitemap has changed

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

Set ``STATICSITEMAPS_ROOT_SITEMAP`` variable in your ``settings.py`` to point to dictionary holding the sitemaps configuration (as seen in Django docs)::

	STATICSITEMAPS_ROOT_SITEMAP = 'myproject.sitemaps.sitemaps'

Include ``static_sitemaps.urls`` to your ``urls.py`` to serve the root ``sitemap.xml`` if you want to serve index file through Django (might be usefull sometimes when it's hard for you to serve it by webserver itself)::
	
	urlpatterns = patterns('',
		url(r'^sitemap.xml', include('static_sitemaps.urls')),
	)

Setup your cron to run::

	django-admin.py refresh_sitemap

periodically. Usually, it's enough to set it to run once by 30 minutes or so.

Done.

Advanced settings
------------------

``STATICSITEMAPS_ROOT_DIR``
    Filesystem path to generate the sitemaps files to. Defaults to ``STATIC_ROOT`` directory.

``STATICSITEMAPS_USE_GZIP``
	Defaults to ``True``. If ``True``, gzip compression will be used when generating the sitemaps files (which is very possible by sitemaps specification).

``STATICSITEMAPS_FILENAME_TEMPLATE``
	Template for sitemap parts. Defaults to ``sitemap-%(section)s-%(page)s.xml``.

``STATICSITEMAPS_SITEMAP_DOMAIN``
	Set this to the domain from which you serve static files in case it it different from domain of your Django application. Defaults to current site's domain.

``STATICSITEMAPS_LANGUAGE``
    Language code to use when generating the sitemaps. Defaults to ``LANGUAGE_CODE`` setting.
    
``STATICSITEMAPS_PING_GOOGLE``
    Boolean determining whether to ping google after sitemaps have been updated. Defaults to ``True``.
