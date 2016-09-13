from django.core.cache.backends.filebased import FileBasedCache


class SmartFileBasedCache(FileBasedCache):
    def _force_cull(self, max_entries):
        self._max_entries = int(max_entries)
        return self._cull()

    def _cull(self):
        if int(self._max_entries) == -1:
            return
        return super(SmartFileBasedCache, self)._cull()
