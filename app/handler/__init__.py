# -*- coding: utf-8 -*-
from django.utils.log import AdminEmailHandler
from redis import ConnectionError, ResponseError
from django.conf import settings
import random


def skip_debug(record):
    return not settings.DEBUG


def skip_redis_connectionerror(record):
    if record.exc_info:
        exc_type, exc_value = record.exc_info[:2]
        if isinstance(exc_value, ConnectionError) or isinstance(exc_value, ResponseError):
            i = random.randint(1, 100)
            if i == 1:
                return True
            return False
    return True


class ThrottledAdminEmailHandler(AdminEmailHandler):
    PERIOD_LENGTH_IN_SECONDS = 300
    MAX_EMAILS_IN_PERIOD = 1
    COUNTER_CACHE_KEY = 'email_admins_counter'

    def increment_counter(self):
        from django.core.cache import get_cache
        cache = get_cache('default')
        try:
            cache.incr(self.COUNTER_CACHE_KEY)
        except ValueError:
            cache.set(self.COUNTER_CACHE_KEY, 1, self.PERIOD_LENGTH_IN_SECONDS)
        return cache.get(self.COUNTER_CACHE_KEY)

    def emit(self, record):
        try:
            counter = self.increment_counter()
        except Exception:
            pass
        else:
            if counter > self.MAX_EMAILS_IN_PERIOD:
                return
        super(ThrottledAdminEmailHandler, self).emit(record)
