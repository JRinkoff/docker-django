from django.core.management.base import BaseCommand
from django.core.cache import caches
import os
import glob
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('clear', nargs='+', type=str, choices=['all', 'default', 'templates', 'cachalot'])

    def clear_templates(self):
        files = glob.glob(os.path.join(__location__, '../../../cache/template_fragments/*.djcache'))
        for f in files:
            os.remove(f)
        print 'Template cache cleared'

    def clear_cache(self, name):
        cache = caches[name]
        keys = cache.delete_many(cache.keys('*'))
        print 'Cache "{name}" cleared. {keys} keys deleted.'.format(name=name, keys=keys)

    def handle(self, *args, **options):
        for clear in options['clear']:
            if clear == 'all':
                self.clear_cache('default')
                if 'templates' not in options['clear']:
                    self.clear_templates()
            elif clear == 'default':
                self.clear_cache('default')
            elif clear == 'cachalot':
                self.clear_cache('cachalot')
            elif clear == 'templates':
                self.clear_templates()
