from fastapi import FastAPI

from server.api.routers import api_router
from server.models import Base
from server.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)
