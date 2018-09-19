from datetime import timedelta

from celery.task import PeriodicTask

from static_sitemaps import conf
from static_sitemaps.generator import generate_sitemap

__author__ = 'xaralis'

# Create class conditionally so the task can be bypassed when repetition 
# is set to something which evaluates to False.
if conf.CELERY_TASK_REPETITION or conf.CELERY_TASK_SCHEDULE:
    class GenerateSitemap(PeriodicTask):

        def __init__(self):
            if conf.CELERY_TASK_REPETITION and conf.CELERY_TASK_SCHEDULE:
                raise ValueError(
                    'You should set one setting of STATICSITEMAPS_REFRESH_AFTER or STATICSITEMAPS_REFRESH_ON')
            if conf.CELERY_TASK_REPETITION:
                self.run_every = timedelta(minutes=conf.CELERY_TASK_REPETITION)
                super().__init__()
            else:
                self.run_every = conf.CELERY_TASK_SCHEDULE
    
        def run(self, **kwargs):
            generate_sitemap(verbosity=1)
