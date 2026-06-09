from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

CALL_COUNT = 0

@app.get("/test")
@limiter.limit("5/minute")
def testusers(request: Request):
    global CALL_COUNT
    CALL_COUNT += 1
    test_users = ["user1", "user2", "user3"]
    return {"test_users": test_users, "call_count": CALL_COUNT}
