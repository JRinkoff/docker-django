from django.utils.cache import add_never_cache_headers


class DisableClientSideCachingMiddleware(object):
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response


class TTLMiddleware(object):
    def process_response(self, request, response):
        if hasattr(response, 'context_data'):
            ttl = response.context_data.get('ttl')
            if ttl:
                response['X-Cache-TTL'] = ttl
        return response


class VaryMiddleware(object):
    def process_response(self, request, response):
        if hasattr(response, 'context_data'):
            vary = response.context_data.get('vary')
            if vary:
                response['X-Cache-Vary'] = vary
        return response
