from django.core.management.base import BaseCommand
from static_sitemaps.generator import generate_sitemap

__author__ = 'xaralis'


class Command(BaseCommand):
    command = None
    help = 'Generates sitemaps files to a predefined directory.'

    def handle(self, *args, **options):
        generate_sitemap(verbosity=int(options.get('verbosity', 0)))
