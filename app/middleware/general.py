from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import Http404
from django.conf import settings
import re


def parse_forwarded_for(forwarded_for):
    # Parses the X-Forwarded-For header from right to left
    # Ignores IP addresses from Proxy to get the first unknown IP address
    # Split the list of X-Forwarded-For addresses
    ips = [ip.strip() for ip in forwarded_for.split(',')]
    # Iterated in reversed order, important because left to right address can be spoofed, so we want to traverse
    # in right to left order.
    for ip in reversed(ips):
        if re.match(settings.DOCKER_IPS, ip):
            # This is a Docker IP address, ignore it
            continue
        else:
            return ip
    return None


class InternalUseOnlyMiddleware(object):
    """
    Middleware to prevent access to the admin if the user IP
    isn't in the INTERNAL_IPS setting.
    """
    def process_request(self, request):
        try:
            admin_index = reverse('admin:index')
        except NoReverseMatch:
            return
        if not request.path.startswith(admin_index) or settings.DEBUG:
            return
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if not forwarded_for:
            raise Http404
        remote_addr = parse_forwarded_for(forwarded_for)
        if not remote_addr:
            raise Http404
        if remote_addr not in settings.INTERNAL_IPS:
            raise Http404
