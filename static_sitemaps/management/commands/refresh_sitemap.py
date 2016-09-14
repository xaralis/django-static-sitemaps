from django.core.management.base import BaseCommand
from static_sitemaps.generator import SitemapGenerator

__author__ = 'xaralis'


class Command(BaseCommand):
    command = None
    help = 'Generates sitemaps files to a predefined directory.'

    def handle(self, *args, **options):
        generator = SitemapGenerator(int(options.get('verbosity', 0)))
        generator.write()
