from fastapi import FastAPI

from database import engine, Base
from middlewares.logging_middleware import log_requests

from routers.user import router as user_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add the logging middleware
app.middleware("http")(log_requests)

# Include routers
app.include_router(user_router)
