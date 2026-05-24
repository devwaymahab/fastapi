from fastapi import FastAPI

from database import engine, Base
from middlewares.logging_middleware import log_requests
from routers.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests)


# Include routers
app.include_router(user_router)
