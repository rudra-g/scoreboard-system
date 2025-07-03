import redis
from django.conf import settings

redis_client = redis.StrictRedis(
    host=getattr(settings, 'REDIS_HOST', 'localhost'),
    port=getattr(settings, 'REDIS_PORT', 6379),
    db=0,
    decode_responses=True
)

def cache_set(key, value, ttl=10):
    redis_client.set(key, value, ex=ttl)

def cache_get(key):
    return redis_client.get(key)

def cache_delete(key):
    redis_client.delete(key)
