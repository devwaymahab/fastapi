# RedisExample

This example shows a simple FastAPI app that caches user data in Redis.

## Requirements

- Python 3.9+
- Docker (for running Redis)

## Install Python dependencies

From the `GITHUB/RedisExample` directory:

```bash
python -m pip install -r requirements.txt
```

## Run Redis with Docker

Start a Redis container on the default port 6379:

```bash
docker run -d --name redis-example -p 6379:6379 redis:latest
```

Verify Redis is running:

```bash
docker ps
```

If you want to stop and remove the container later:

```bash
docker stop redis-example

docker rm redis-example
```

## Run the FastAPI app

From the `GITHUB/RedisExample` directory:

```bash
uvicorn main:app --reload
```

The app will be available at `http://127.0.0.1:8000`.

## Test the endpoint

Fetch user data with the cache flow:

```bash
curl http://127.0.0.1:8000/users/1
```

- The first request is a cache miss and takes longer, retrieving data from `db.py`.
- Subsequent requests within 60 seconds are cache hits and return Redis data quickly.

## Notes

- Redis is configured in `redis_client.py` to connect to `localhost:6379`.
- Cached values expire after 60 seconds.
