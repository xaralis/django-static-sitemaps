"""
Reusable app meant to allow users to serve sitemap files by webserver
instead of Django and generate sitemaps by running cron command.

This results in better performance for sites with loads of content and/or URLS.

App is dependent on original django.contrib.sitemaps application which
has to be included in order for this to work.
"""
__versionstr__ = '4.5.0'
