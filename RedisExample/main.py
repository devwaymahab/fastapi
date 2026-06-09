import json
from time import time

from fastapi import FastAPI

from db import get_user_from_db
from redis_client import redis_client

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Check if user data is in Redis cache - CACHE HIT
    cache_key = f"user:{user_id}"

    cached_user = redis_client.get(cache_key)

    if cached_user:
        print("Fetching from Redis...")
        return json.loads(cached_user)
    
    # If not in cache, fetch from DB - CACHE MISS
    user = get_user_from_db(user_id)
    
    # Store user data in Redis cache
    redis_client.set(
        cache_key,
        json.dumps(user),
        ex=60  # Cache expires in 60 seconds
    )

    return user