import time

from fastapi import Request


async def log_requests(request: Request, call_next):

    start = time.time()

    print("REQUEST PATH:", request.url.path)

    response = await call_next(request)

    process_time = time.time() - start

    print("TIME TAKEN:", process_time)

    return response
