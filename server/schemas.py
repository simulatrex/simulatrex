from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    avatar_url: Optional[str] = None


class SimulationBase(BaseModel):
    name: str
    description: str
    author: str
    config: str


class Simulation(SimulationBase):
    id: str


class SimulationCreate(SimulationBase):
    pass


class SimulationLog(BaseModel):
    id: str
    simulation_id: str
    timestamp: str
    message: str
