import os
import redis
import random

r = redis.Redis()
random.seed(444)
#r = redis.from_url(os.environ.get("REDIS_URL", None))

hats = {f"hat:{random.getrandbits(32)}": i for i in (
   {
        "color": "black",
        "price": 49.99,
        "style": "fitted",
        "quantity": 1000,
        "npurchased": 0,
    },
    {
        "color": "maroon",
        "price": 59.99,
        "style": "hipster",
        "quantity": 500,
        "npurchased": 0,
    },
    {
        "color": "green",
        "price": 99.99,
        "style": "baseball",
        "quantity": 200,
        "npurchased": 0,
    })
}

if __name__ == '__main__':
    print(r.keys())