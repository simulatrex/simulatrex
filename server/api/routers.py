from fastapi import APIRouter

from server.api.endpoints import user, simulation

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(
    simulation.router, prefix="/simulations", tags=["simulations"]
)
