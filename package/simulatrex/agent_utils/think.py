"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: think.py
Description: Think and create memories based  on environment settings

"""
from simulatrex.memory import MemoryUnitModel
from simulatrex.environment import BaseEnvironment
from simulatrex.config import AgentIdentity
from simulatrex.llm_utils.prompts import PromptManager, TemplateType
from simulatrex.llm_utils.models import BaseLanguageModel
from simulatrex.utils.log import SingletonLogger
from .types import AgentMemory

_logger = SingletonLogger


async def think(
    cognitive_model: BaseLanguageModel,
    memory: AgentMemory,
    identity: AgentIdentity,
    environment: BaseEnvironment,
):
    """
    Think and create memories based  on environment settings
    """
    prompt = PromptManager().get_filled_template(
        TemplateType.AGENT_THINK,
        name=identity.name,
        age=identity.age,
        gender=identity.gender,
        persona=identity.persona,
        ethnicity=identity.ethnicity,
        language=identity.language,
        core_memories=", ".join(identity.core_memories),
        environment_context=environment.context,
        environment_description=environment.description,
        environment_entities=", ".join(environment.entities),
    )

    response = await cognitive_model.generate_structured_output(prompt, MemoryUnitModel)

    _logger.debug(f"Agent {identity.name} thought: {response}")

    _memory = MemoryUnitModel(
        **response.dict(),
    )
    _memory.created = environment.get_current_time()
    _memory.last_accessed = environment.get_current_time()

    memory.short_term_memory.add_memory(_memory)
    memory.long_term_memory.add_memory(_memory)

    _logger.debug(f"Current thought: {response.content}")
