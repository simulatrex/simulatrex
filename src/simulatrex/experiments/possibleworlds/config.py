"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: config.py
Description: Defines a config for a simulation

"""

from pydantic import BaseModel
from typing import List, Dict, Optional, Union


class Objective(BaseModel):
    id: str
    description: str
    metric: Optional[str] = None
    target: str


class ResponseModel(BaseModel):
    type: str
    parameters: Dict[str, float]


class AgentIdentity(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    ethnicity: Optional[str] = None
    language: Optional[str] = None
    persona: Optional[str] = None
    personality_description: Optional[str] = None
    traits: List[str] = []
    interests: List[str] = []
    knowledge_base: List[str] = []
    skills: List[str] = []
    behavior_patterns: List[str] = []
    past_experiences: List[str] = []
    societal_role: Optional[str] = None
    affiliations: List[str] = []
    current_state: Optional[str] = None
    core_memories: List[str] = []


class InitialConditions(BaseModel):
    awareness: Optional[float] = None


class TargetGroupRelationship(BaseModel):
    target_group_id: str  # ID of the other agent in this relationship
    type: str  # E.g., "friend", "colleague"
    strength: float  # E.g., from 0 (acquaintance) to 1 (best friend)


class AgentRelationship(BaseModel):
    agent_id: str  # ID of the other agent in this relationship
    type: str  # E.g., "friend", "colleague"
    strength: float  # E.g., from 0 (acquaintance) to 1 (best friend)

    def summary(self) -> str:
        return f"{self.type.capitalize()} with {self.agent_id} at a strength level of {self.strength}"


class AgentGroup(BaseModel):
    id: str
    type: str  # E.g., "school", "company"
    member_agent_ids: List[str]
    metadata: Optional[Dict[str, Union[str, int, float]]]


class Agent(BaseModel):
    id: str
    type: str
    identity: AgentIdentity
    initial_conditions: InitialConditions
    cognitive_model: str
    relationships: List[AgentRelationship]
    group_affiliations: List[str]


class AgentsHierarchy(BaseModel):
    organizations: List[Dict[str, Union[str, List[str]]]]


class MappingRule(BaseModel):
    csv_column: str
    agent_attribute: str


class DataFeed(BaseModel):
    type: str
    location: str
    mapping_rules: List[MappingRule]


class SimulationTimeConfig(BaseModel):
    start_time: str
    end_time: str
    time_multiplier: int


class Environment(BaseModel):
    type: str
    description: str
    context: str
    entities: List[str]
    time_config: SimulationTimeConfig
    # data_feed: Union[None, DataFeed]


class Event(BaseModel):
    id: str
    type: str
    source: str
    content: str
    impact: Optional[float] = None
    scheduled_time: str


class Evaluation(BaseModel):
    metrics: List[str]
    objectives: List[Objective]


class ExpectedOutcome(BaseModel):
    average_awareness_level: float
    highest_influence_platform: str
    agent_collaboration_count: int


class TargetGroup(BaseModel):
    id: str
    role: str
    responsibilities: str
    initial_conditions: Optional[InitialConditions] = None
    num_agents: int = 1
    relationships: Optional[List[TargetGroupRelationship]] = None


class SimulationConfig(BaseModel):
    title: str
    environment: Environment
    agents: Optional[List[Agent]] = None
    groups: Optional[List[AgentGroup]] = None
    target_groups: Optional[List[TargetGroup]] = None
    events: List[Event]
    evaluation: Evaluation


class Config(BaseModel):
    version: str
    simulation: SimulationConfig
