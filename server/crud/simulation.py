import json
import dotenv
from fastapi import WebSocket
from simulatrex.engine import SimulationEngine
from sqlalchemy.orm import Session

from server import models, schemas

dotenv.load_dotenv()


def fetch_simulations(db: Session):
    """Fetch all simulations."""
    return db.query(models.Simulation).all()


def create_simulation(db: Session, simulation: schemas.SimulationCreate):
    """Create a new simulation."""
    db_simulation = models.Simulation(
        id="new_id",
        name=simulation.name,
        description=simulation.description,
        author=simulation.author,
        config=simulation.config,
    )
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    return db_simulation


def query_simulation(db: Session, simulation_id: str):
    """Query a simulation by ID."""
    return (
        db.query(models.Simulation)
        .filter(models.Simulation.id == simulation_id)
        .first()
    )


async def run_simulation(websocket: WebSocket, db: Session, simulation_id: str):
    """Run a simulation by ID."""
    sim = (
        db.query(models.Simulation)
        .filter(models.Simulation.id == simulation_id)
        .first()
    )

    json_config = json.loads(sim.config)
    engine = SimulationEngine(config=json_config)

    async for log in engine.run():
        print(log)
        await websocket.send_text(log)

    return sim


def query_simulation_logs(db: Session, simulation_id: str):
    """Query a simulation's logs by ID."""
    return (
        db.query(models.SimulationLog)
        .filter(models.SimulationLog.simulation_id == simulation_id)
        .all()
    )
