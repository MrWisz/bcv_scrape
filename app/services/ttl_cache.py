"""
In-process TTL cache for expensive live scrape/API calls.

The app runs as a single gunicorn worker (see render.yaml), so a plain
module-level dict is sufficient - no cross-process synchronization needed.
"""
import time


class TTLCache:
    def __init__(self, ttl_seconds):
        self.ttl_seconds = ttl_seconds
        self._store = {}

    def get(self, key):
        """
        Returns:
            tuple: (value, is_fresh). value is None if the key was never set.
        """
        entry = self._store.get(key)
        if not entry:
            return None, False

        is_fresh = (time.time() - entry['timestamp']) < self.ttl_seconds
        return entry['value'], is_fresh

    def set(self, key, value):
        self._store[key] = {'value': value, 'timestamp': time.time()}
