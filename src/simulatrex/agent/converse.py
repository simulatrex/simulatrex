"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: converse.py
Description: Converse for inter-agent communication

"""
from simulatrex.experiments.possibleworlds.environment import BaseEnvironment
from simulatrex.experiments.possibleworlds.config import AgentIdentity
from simulatrex.agent.utils.types import AgentMemory
from simulatrex.llm_utils.prompts import PromptManager, TemplateType
from simulatrex.llm_utils.models import BaseLanguageModel
from simulatrex.utils.log import SingletonLogger

_logger = SingletonLogger


async def converse(
    cognitive_model: BaseLanguageModel,
    memory: tuple[AgentMemory],
    identities: tuple[AgentIdentity],
    environment: BaseEnvironment,
    topic: str,
):
    """
    Converse on a given topic
    """

    # Converse about a current topic
    prompt = PromptManager().get_filled_template(
        TemplateType.AGENT_CONVERSE,
        agent1_name=identities[0].name,
        agent1_age=identities[0].age,
        agent1_gender=identities[0].gender,
        agent1_persona=identities[0].persona,
        agent1_memories=", ".join(identities[0].core_memories),
        agent2_name=identities[1].name,
        agent2_age=identities[1].age,
        agent2_gender=identities[1].gender,
        agent2_persona=identities[1].persona,
        agent2_core_memories=", ".join(identities[1].core_memories),
        environment_context=environment.context,
        topic=topic,
    )

    try:
        response = await cognitive_model.ask(prompt)
    except Exception as e:
        _logger.error(f"Error while asking LLM: {e}")

        # Try request again
        response = await cognitive_model.ask(prompt)

    _logger.debug(response)

    return response
