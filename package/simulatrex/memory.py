"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: memory.py
Description: Defines the memory class, which is used to define the memory of an agent

"""
from datetime import timedelta
import uuid

from pydantic import BaseModel

from simulatrex.db import SqliteDB, MemoryUnitDB
from simulatrex.utils.log import SingletonLogger
from simulatrex.vectordb import VectorDB

_logger = SingletonLogger


class MemoryUnitModel(BaseModel):
    type: str
    depth: float
    content: str
    keywords: str
    id: str

    score: float = 0.0
    created: int = 0
    last_accessed: int = 0

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid.uuid4())

    def get_metadata(self):
        return {
            "id": self.id,
            "type": self.type,
            "depth": self.depth,
            "created": self.created,
            "last_accessed": self.last_accessed,
            "keywords": self.keywords,
            "score": self.score,
        }


class ShortTermMemory:
    def __init__(self, id: str, decay_factor: int):
        stm_id = "stm_" + id
        self.vector_db = VectorDB(stm_id)
        self.decay_factor = decay_factor

    def add_memory(self, memory_unit: MemoryUnitModel):
        _logger.debug(f"Adding STM memory with id {memory_unit.id}")
        self.vector_db.add_memory(
            memory_unit.content,
            metadatas=[memory_unit.get_metadata()],
            ids=[memory_unit.id],
        )

    def retrieve_memory(
        self, content: str, n_results: int, current_timestamp: int, time_multiplier: int
    ):
        query_results = self.vector_db.query_memory(content, n_results=n_results)
        metadata_entries = query_results["metadatas"][0]
        results = []

        # Apply decay factor to the results based on the 'created' date
        for i, metadata in enumerate(metadata_entries):
            _logger.debug(f"Metadata: {metadata}")
            time_diff = (
                current_timestamp - metadata["last_accessed"]
            ) / time_multiplier

            decay = 1 / (1 + self.decay_factor * time_diff)
            metadata["score"] *= decay
            _logger.debug(f"Score: {metadata['score']}")

            content = query_results["documents"][0][i]

            memory = MemoryUnitModel(
                id=metadata["id"],
                type=metadata["type"],
                depth=metadata["depth"],
                content=content,
                keywords=metadata["keywords"],
                score=metadata["score"],
                created=metadata["created"],
                last_accessed=current_timestamp,
            )
            results.append(memory)

        # Sort the results by score in descending order
        results.sort(key=lambda x: x.score, reverse=True)
        return results


class LongTermMemory:
    def __init__(self, id: str):
        ltm_id = "ltm_" + id
        self.db = SqliteDB(ltm_id)

    def add_memory(self, memory_unit: MemoryUnitModel):
        memory_unit_db = MemoryUnitDB(**memory_unit.model_dump())
        _logger.debug(f"Adding LTM memory with id {memory_unit_db.id}")
        self.db.insert_memory(memory_unit_db)

    def query_memory_by_type(self, type: str, n_results: int = 5):
        return self.db.query_memory_by_type(type, n_results)
