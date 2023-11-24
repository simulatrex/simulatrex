from typing import List
from fastapi import APIRouter, Depends, Path, WebSocket
from sqlalchemy.orm import Session

from server import schemas, dependencies
from server.crud import simulation as crud

router = APIRouter()


@router.get("/", response_model=List[schemas.Simulation])
async def fetch_simulations(db: Session = Depends(dependencies.get_db)):
    return crud.fetch_simulations(db=db)


@router.post("/", response_model=schemas.SimulationBase)
async def create_simulation(
    simulation: schemas.SimulationCreate, db: Session = Depends(dependencies.get_db)
):
    return crud.create_simulation(db=db, simulation=simulation)


@router.get("/{simulation_id}", response_model=schemas.Simulation)
async def get_simulation(
    simulation_id: str = Path(..., title="The ID of the simulation to get"),
    db: Session = Depends(dependencies.get_db),
):
    return crud.query_simulation(db=db, simulation_id=simulation_id)


@router.websocket("/{simulation_id}/run")
async def run_simulation(
    websocket: WebSocket,
    simulation_id: str = Path(..., title="The ID of the simulation to get"),
    db: Session = Depends(dependencies.get_db),
):
    await websocket.accept()
    res = await crud.run_simulation(websocket, db=db, simulation_id=simulation_id)
    await websocket.send_json(res)


@router.get("/{simulation_id}/logs", response_model=List[schemas.SimulationLog])
async def get_simulation_logs(
    simulation_id: str = Path(..., title="The ID of the simulation to get logs for"),
    db: Session = Depends(dependencies.get_db),
):
    return crud.query_simulation_logs(db=db, simulation_id=simulation_id)
