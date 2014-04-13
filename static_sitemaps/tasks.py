from datetime import timedelta

from celery.task import PeriodicTask

from static_sitemaps import conf
from static_sitemaps.generator import SitemapGenerator

__author__ = 'xaralis'


class GenerateSitemap(PeriodicTask):
    run_every = timedelta(minutes=conf.CELERY_TASK_REPETITION)

    def run(self, **kwargs):
        generator = SitemapGenerator(verbosity=1)
        generator.write()

