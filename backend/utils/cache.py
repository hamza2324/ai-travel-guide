from cachetools import TTLCache

geocode_cache: TTLCache = TTLCache(maxsize=256, ttl=60 * 60 * 12)
places_cache: TTLCache = TTLCache(maxsize=128, ttl=60 * 45)
route_cache: TTLCache = TTLCache(maxsize=256, ttl=60 * 60)
wiki_cache: TTLCache = TTLCache(maxsize=256, ttl=60 * 60 * 24)
