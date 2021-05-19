import os
import redis

REDIS_URL = os.environ.get("REDIS_URL", None)
if REDIS_URL is not None:
    token_watcher = redis.from_url(REDIS_URL, db=1)
    country_watcher = redis.from_url(REDIS_URL, db=0)
    contact_cache = redis.from_url(REDIS_URL, db=2)
else:
    token_watcher = redis.Redis(db=1)
    country_watcher = redis.Redis(host='127.0.0.1', port=9851, db=0)
    contact_cache = redis.Redis(db=2)
