"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: agent.py
Description: Defines an agent, central unit in our simulation

"""
from typing import List
import uuid
from pydantic import BaseModel

from simulatrex.environment import BaseEnvironment
from simulatrex.config import (
    AgentIdentity,
    InitialConditions,
    AgentRelationship,
    AgentGroup,
    Objective,
)
from simulatrex.agent_utils.types import AgentType, AgentMemory, CognitiveModel
from simulatrex.agent_utils.perceive import perceive
from simulatrex.agent_utils.think import think
from simulatrex.event import Event
from simulatrex.utils.log import SingletonLogger
from simulatrex.llm_utils.models import OpenAILanguageModel, LlamaLanguageModel
from simulatrex.llm_utils.prompts import PromptManager, TemplateType

_logger = SingletonLogger


class Message:
    def __init__(
        self,
        sender_id: str,
        receiver_id: str,
        content: str,
        group_id: str = None,
        metadata: any = {},
    ):
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.group_id = group_id
        self.metadata = metadata


class BaseAgent:
    def __init__(
        self,
        id: str,
        type: AgentType,
        identity: AgentIdentity,
        initial_conditions: InitialConditions,
    ):
        self.id = "agent_" + id
        self.type = type

        self.identity = identity
        self.initial_conditions = initial_conditions

        self.relationships: List[AgentRelationship] = []
        self.groups: List[AgentGroup] = []

        self.memory = AgentMemory(
            self.id,
            decay_factor=initial_conditions["decay_factor"]
            if initial_conditions and "decay_factor" in initial_conditions
            else 0.995,
        )


class LLMAgent(BaseAgent):
    def __init__(
        self,
        id: str,
        type: AgentType,
        identity: AgentIdentity,
        initial_conditions: InitialConditions,
        cognitive_model_id: str,
    ):
        super().__init__(id, type, identity, initial_conditions)

        self.cognitive_model_id = cognitive_model_id
        self.cognitive_model = None
        self.message_queue: List[Message] = []

        _logger.debug(
            f"Agent {self.id} is using cognitive model {self.cognitive_model_id}"
        )
        self._init_cognition()

    def _init_cognition(self):
        if self.cognitive_model_id == CognitiveModel.GPT_4_TURBO.value:
            self.cognitive_model = OpenAILanguageModel(
                model_id=CognitiveModel.GPT_4_TURBO, agent_id=self.id
            )
        elif self.cognitive_model_id == CognitiveModel.GPT_4.value:
            self.cognitive_model = OpenAILanguageModel(
                model_id=CognitiveModel.GPT_4, agent_id=self.id
            )
        elif self.cognitive_model_id == CognitiveModel.LLAMA_2_70b.value:
            self.cognitive_model = LlamaLanguageModel(
                model_id=CognitiveModel.LLAMA_2_70b, agent_id=self.id
            )
        else:
            raise NotImplementedError(
                f"Model {self.cognitive_model_id} not implemented yet"
            )

    async def perceive_event(
        self,
        event: Event,
        environment: BaseEnvironment,
    ):
        _logger.debug(f"Agent {self.id} is processing event {event.id}")
        await perceive(
            self.cognitive_model,
            self.memory,
            self.identity,
            environment,
            event,
        )

    async def think(self, environment: BaseEnvironment):
        # Based on the provided envrioment make some thoughts
        await think(self.cognitive_model, self.memory, self.identity, environment)

    async def evaluate_outputs(
        self, environment: BaseEnvironment, objective: Objective
    ):
        _logger.debug(f"Agent {self.id} is evaluating outputs")
        # Based on agent memory and environment, evaluate outputs
        prompt = PromptManager().get_filled_template(
            TemplateType.AGENT_EVALUATION,
            agent_name=self.identity.name,
            agent_output=self.memory.long_term_memory.query_memory_by_type(
                "thought", n_results=8
            ),
            environment=environment,
            objective=objective,
        )

        response = await self.cognitive_model.ask(prompt)
        return response

    class AgentConverseResponseModel(BaseModel):
        should_converse: bool
        receiver_ids: List[str]

    async def initiate_conversation(self, environment: BaseEnvironment):
        # Use the cognitive model to decide when to send a message and what the content should be
        reponse = await self._decide_on_converse(environment)
        if reponse.should_converse:
            content = await self._generate_message_content(environment)
            await self._send_message(reponse.receiver_ids, content)

    async def _generate_message_content(self, environment: BaseEnvironment) -> str:
        # Generate a message based on the agent memory and environment
        prompt = PromptManager().get_filled_template(
            TemplateType.AGENT_START_CONVERSATION,
            last_memory=self.memory.long_term_memory.query_memory_by_type(
                "thought", n_results=1
            ),
            agent_name=self.identity.name,
            environment=environment,
        )

        response = await self.cognitive_model.ask(prompt)
        return response

    async def _decide_on_converse(
        self, environment: BaseEnvironment
    ) -> AgentConverseResponseModel:
        # Use the cognitive model to decide when to send a message
        _logger.debug(f"Agent {self.id} is deciding whether to send a message")

        last_thoughts = self.memory.long_term_memory.query_memory_by_type(
            "thought", n_results=3
        )

        agent_thoughts = []
        for thought in last_thoughts:
            agent_thoughts.append(thought.content)

        agent_relationships = []
        for relationship in self.relationships:
            _logger.debug(relationship.summary())
            agent_relationships.append(relationship.summary())

        if agent_relationships:
            _logger.info(f"Relationships found for the agent: {agent_relationships}")
            prompt = PromptManager().get_filled_template(
                TemplateType.AGENT_DECIDE_ON_CONVERSATION,
                agent_name=self.identity.name,
                agent_thoughts=agent_thoughts,
                agent_relationships=agent_relationships,
                environment=environment,
            )

            response = await self.cognitive_model.generate_structured_output(
                prompt, response_model=self.AgentConverseResponseModel
            )

            if response.should_converse:
                _logger.info(f"Agent {self.id} decided to start a conversation")
            else:
                _logger.info(f"Agent {self.id} decided not to start a conversation")

            return response

        else:
            _logger.info(f"No relationships found for the agent")
            return self.AgentConverseResponseModel(
                should_converse=False, receiver_ids=[]
            )

    def _send_message(self, receiver_id: str, content: str):
        message = Message(self.id, receiver_id, content)
        return message

    async def _process_messages(self):
        for message in self.message_queue:
            # Use the cognitive model to produce results
            converse_prompt = PromptManager().get_filled_template(
                TemplateType.AGENT_REPLY_TO_CONVERSATION,
                name=self.identity.name,
                age=self.identity.age,
                gender=self.identity.gender,
                persona=self.identity.persona,
                ethnicity=self.identity.ethnicity,
                language=self.identity.language,
                core_memories=", ".join(self.identity.core_memories),
                sender_identity=message.metadata,
                received_message=message.content,
            )

            response_content = await self.cognitive_model.ask(converse_prompt)

            # Send a reply message
            self._send_message(message.sender_id, response_content)

            # Remove current message object from queue
            self.message_queue = [
                msg for msg in self.message_queue if msg.id != message.id
            ]
