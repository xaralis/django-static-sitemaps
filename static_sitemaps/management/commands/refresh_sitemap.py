from django.core.management.base import NoArgsCommand

from static_sitemaps.generator import SitemapGenerator

__author__ = 'xaralis'


class Command(NoArgsCommand):
    command = None
    help = 'Generates sitemaps files to a predefined directory.'

    def handle_noargs(self, **options):
        generator = SitemapGenerator(int(options.get('verbosity', 0)))
        generator.write()
