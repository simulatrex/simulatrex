from sqlalchemy import Column, Integer, String

from server.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    avatar_url = Column(String)


class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    author = Column(String)
    config = Column(String)


class SimulationLog(Base):
    __tablename__ = "simulation_logs"

    id = Column(String, primary_key=True, index=True)
    simulation_id = Column(String, index=True)
    timestamp = Column(String)
    message = Column(String)
