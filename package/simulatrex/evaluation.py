"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: evaluation.py
Description: Evaluation Processor

"""
from typing import List

from simulatrex.agent import LLMAgent
from simulatrex.config import Evaluation
from simulatrex.environment import BaseEnvironment
from simulatrex.llm_utils.prompts import PromptManager, TemplateType
from simulatrex.llm_utils.models import OpenAILanguageModel
from simulatrex.agent_utils.types import CognitiveModel


class Objective:
    def __init__(self, id: str, description: str, metric: str, target: str):
        self.id = id
        self.description = description
        self.metric = metric
        self.target = target


class EvaluationEngine:
    def __init__(self, evaluation: Evaluation):
        self.metrics = evaluation.metrics
        self.objectives = [
            Objective(obj.id, obj.description, obj.metric, obj.target)
            for obj in evaluation.objectives
        ]

        self.llm = OpenAILanguageModel(model_id=CognitiveModel.GPT_4)
        self.prompt_manager = PromptManager()

    async def evaluate_agents_outputs(
        self,
        agents: List[LLMAgent],
        environment: BaseEnvironment,
    ):
        agent_results = ""
        results = []

        for objective in self.objectives:
            for agent in agents:
                agent_result = await agent.evaluate_outputs(environment, objective)
                agent_results += agent_result + "\n\n"

            prompt = self.prompt_manager.get_filled_template(
                TemplateType.EVALUATE_AGENT_OUTPUTS,
                agent_results=agent_results,
                environment=environment,
                objective=objective,
            )

            llm_response = await self.llm.ask(prompt)

            results.append(
                {
                    "objective_id": objective.id,
                    "description": objective.description,
                    "llm_response": llm_response,
                }
            )

        return results
