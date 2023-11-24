"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: environment.py
Description: Defines the environment class, with a base environment and a dynamic and static environment

"""
from datetime import timedelta
from enum import Enum
from typing import List

from simulatrex.agent_utils.types import CognitiveModel
from simulatrex.llm_utils.models import OpenAILanguageModel
from simulatrex.llm_utils.prompts import PromptManager, TemplateType
from simulatrex.utils.time_utils import TimeUtils
from simulatrex.event import Event, EventEngine
from simulatrex.config import SimulationTimeConfig


class EnvironmentType(Enum):
    Dynamic = "DYNAMIC"
    Static = "STATIC"


class BaseEnvironment:
    def __init__(
        self, description: str, context: str, entities: List[str], events: List[any]
    ):
        self.description = description
        self.context = context  # Contextual information about the environment
        self.entities = entities

        self.event_engine = self.init_event_engine(
            events
        )  # Initialize events from JSON

        self.current_time = 0
        self.start_time = 0
        self.end_time = 0
        self.type = EnvironmentType.Static

        self.llm = OpenAILanguageModel(model_id=CognitiveModel.GPT_4)

    def init_event_engine(self, events: List[any]):
        event_engine = EventEngine(events)
        return event_engine

    def init_time(self, time_config: SimulationTimeConfig):
        self.start_time = TimeUtils.to_timestamp(time_config.start_time)
        self.end_time = TimeUtils.to_timestamp(time_config.end_time)

        self.time_multiplier = time_config.time_multiplier
        self.current_time = self.start_time

    def get_current_time(self):
        return self.current_time

    def is_running(self):
        return self.current_time < self.end_time

    async def update(self) -> tuple[List[Event], str]:
        # Store the previous time before updating the current_time
        previous_time = self.current_time

        # Increase time
        time_step = timedelta(seconds=1).total_seconds() * self.time_multiplier
        self.current_time += time_step

        # Process events
        active_events = self.event_engine.process_events(
            previous_time, self.current_time
        )

        # Summarize the current context
        current_env_context = await self.summarize_context(active_events)

        # Update current env context
        self.context = current_env_context

        return (active_events, current_env_context)

    async def summarize_context(self, active_events: List[Event]):
        # Process current events and summarize the context
        summarize_env_prompt = PromptManager().get_filled_template(
            TemplateType.SUMMARIZE_ENVIRONMENT,
            environment_type=self.type.value,
            environment_context=self.context,
            environment_entities=", ".join(self.entities),
            environment_description=self.description,
            events_summary=", ".join([event.content for event in active_events]),
        )

        response = await self.llm.ask(summarize_env_prompt)
        return response

    def get_recent_events(self, max_events=5):
        return self.event_engine.get_recent_events(max_events)


class StaticEnvironment(BaseEnvironment):
    def __init__(
        self, description: str, context: str, entities: List[str], events: List[any]
    ):
        super().__init__(description, context, entities, events)
        self.type = EnvironmentType.Static


class DynamicEnvironment(BaseEnvironment):
    def __init__(
        self, description: str, context: str, entities: List[str], events: List[any]
    ):
        super().__init__(description, context, entities, events)
        self.type = EnvironmentType.Dynamic
