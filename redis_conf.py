import os
import redis
import random

REDIS_URL = os.environ.get("REDIS_URL", None)
if REDIS_URL is not None:
    token_watcher = redis.from_url(REDIS_URL, db=1)
else:
    token_watcher = redis.Redis(db=1)
