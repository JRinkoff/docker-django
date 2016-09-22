from django.core.management.base import BaseCommand
from subprocess import call
from django.core.cache import caches
import os, glob
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('clear', type=str, choices=['all', 'default', 'templates', 'cachalot', 'varnish', 'redis'])

    def clear_templates(self):
        files = glob.glob(os.path.join(__location__, '../../../cache/template_fragments/*.djcache'))
        for f in files:
            os.remove(f)
        print 'Template cache cleared'

    def clear_cache(self, name):
        cache = caches[name]
        keys = cache.delete_many(cache.keys('*'))
        print 'Cache "{name}" cleared. {keys} keys deleted.'.format(name=name, keys=keys)

    def clear_varnish(self):
        call(['varnishadm', '-T', 'varnish:6082', '-S', '/app/docker/varnish/secret', 'ban.url', '.'])
        print 'Varnish cleared'

    def clear_redis(self):
        call(['redis-cli', '-s', '/app/docker/etc/redis.sock', 'flushall'])
        print 'Redis cleared'

    def handle(self, *args, **options):
        if options['clear'] == 'all':
            self.clear_cache('default')
            self.clear_cache('cachalot')
            self.clear_templates()
            self.clear_redis()
            self.clear_varnish()
        elif options['clear'] == 'default':
            self.clear_cache('default')
        elif options['clear'] == 'cachalot':
            self.clear_cache('cachalot')
        elif options['clear'] == 'templates':
            self.clear_templates()
        elif options['clear'] == 'varnish':
            self.clear_varnish()
        elif options['clear'] == 'redis':
            self.clear_redis()
