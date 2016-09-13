from django.core.management.base import NoArgsCommand
from django.core.cache import caches
from optparse import make_option


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--max_entries', '-m', default=-1, dest='max_entries',
            help='Sets the number of entries to reduce the cache size down to.'), )

    def handle_noargs(self, *args, **options):
        cache = caches['template_fragments']
        max_entries = options.get('max_entries', -1)
        try:
            return cache._force_cull(int(max_entries))
        except AttributeError:
            return None
