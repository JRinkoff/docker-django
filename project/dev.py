from settings import *
from fnmatch import fnmatch


class GlobList(list):
    def __contains__(self, key):
        for elt in self:
            if fnmatch(key, elt):
                return True
        return False

# Support wildcard for internal IP's
INTERNAL_IPS = GlobList(['127.0.0.1', '172.17.0.*'])

ALLOWED_HOSTS += ['.{{project}}.dev']

DEBUG = True
