from datetime import timedelta

from celery.task import PeriodicTask

from static_sitemaps import conf
from static_sitemaps.generator import SitemapGenerator

__author__ = 'xaralis'

# Create class conditionally so the task can be bypassed when repetition 
# is set to something which evaluates to False.
if conf.CELERY_TASK_REPETITION:
    class GenerateSitemap(PeriodicTask):
        run_every = timedelta(minutes=conf.CELERY_TASK_REPETITION)
    
        def run(self, **kwargs):
            generator = SitemapGenerator(verbosity=1)
            generator.write()

