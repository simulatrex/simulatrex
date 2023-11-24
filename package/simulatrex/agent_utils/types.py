"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: types.py
Description: Shared agent types

"""
from enum import Enum
from typing import Dict, List

from simulatrex.memory import LongTermMemory, ShortTermMemory


class AgentType(Enum):
    LLMAgent = "LLM_AGENT"


class CognitiveModel(Enum):
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-1106-preview"
    LLAMA_2_70b = "Llama2_70b"


class AgentMemory:
    def __init__(self, id: str, decay_factor: int) -> None:
        self.decay_factor = decay_factor
        self.short_term_memory = ShortTermMemory(id, decay_factor)
        self.long_term_memory = LongTermMemory(id)
