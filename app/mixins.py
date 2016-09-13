class TTLMixin(object):
    """ Sets the TTL of a view
    """
    ttl = '0s'

    def get_context_data(self, **kwargs):
        context = super(TTLMixin, self).get_context_data(**kwargs)
        context['ttl'] = self.get_ttl()
        return context

    def get_ttl(self):
        return self.ttl


class VaryMixin(object):
    """ Sets the Vary of a view
    """
    vary = 'Accept-Encoding'

    def get_context_data(self, **kwargs):
        context = super(VaryMixin, self).get_context_data(**kwargs)
        context['vary'] = self.get_vary()
        return context

    def get_vary(self):
        return self.vary

