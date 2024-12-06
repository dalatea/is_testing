from .connection import RedisCache
from flask import current_app


_redis_cache = RedisCache(current_app.config['cache_config']) #достать config из current_app
def cached_result(key):
    def decorator(func):
        def wrapper(*args, **kwargs):
            _redis_cache.reconnect_if_need()
            if cache_data := _redis_cache.read(key):
                return cache_data
            response = func(*args, **kwargs)
            _redis_cache.save(response, key)
            return response