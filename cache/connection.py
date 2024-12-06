import redis
import json

class RedisCache:
    def __init__(self, config):
        self.config = config
        self._conn = self._connect()
    def _connect(self):
        return redis.Redis(**self.config)
    def reconnect_if_need(self):
        try:
            _ = self._conn.ping()
        except:
            self._conn = self._connect()
    def save(self, key, value):
        self._conn.set(key, value=json.dumps(value))
    def read(self, key):
        return self._conn.get(key)
