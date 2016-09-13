from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import Http404
from django.conf import settings


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
        if not request.path.startswith(admin_index):
            return
        remote_addr = request.META.get(
            'HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', None))
        ip = remote_addr.replace(', 127.0.0.1', '')
        ip = ip.replace(', 172.17.0.6', '')
        if ip not in settings.INTERNAL_IPS:
            raise Http404
