"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: target_group.py
Description: Target Group Class

"""
import asyncio
from typing import Any, List, Optional
from simulatrex.agent.agent import LLMAgent
from simulatrex.agent.spawn import spawn_agent
from simulatrex.agent.utils.types import CognitiveModel
from simulatrex.llm_utils.models import OpenAILanguageModel


class TargetAudience:
    def __init__(
        self,
        id: str,
    ):
        self.id = id
        self.attributes = {}
        self.cognitive_model_id = "gpt-4-1106-preview"
        self.agents: List[LLMAgent] = []

    def age_range(self, min_age: int, max_age: int):
        self.attributes["age_range"] = (min_age, max_age)
        return self

    def interests(self, interests_list: List[str]):
        self.attributes["interests"] = interests_list
        return self

    def location(self, location: str):
        self.attributes["location"] = location
        return self

    def income_range(self, min_income: float, max_income: float):
        self.attributes["income_range"] = (min_income, max_income)
        return self

    def education_level(self, education_level: str):
        self.attributes["education_level"] = education_level
        return self

    def ethnicity(self, ethnicity: str):
        self.attributes["ethnicity"] = ethnicity
        return self

    def gender(self, gender: str):
        self.attributes["gender"] = gender
        return self

    def occupation(self, occupation: str):
        self.attributes["occupation"] = occupation
        return self

    def family_structure(self, family_structure: str):
        self.attributes["family_structure"] = family_structure
        return self

    def personality_traits(self, traits: List[str]):
        self.attributes["personality_traits"] = traits
        return self

    def values_and_attitudes(self, values: List[str]):
        self.attributes["values_and_attitudes"] = values
        return self

    def lifestyles(self, lifestyles: List[str]):
        self.attributes["lifestyles"] = lifestyles
        return self

    def purchasing_habits(self, habits: List[str]):
        self.attributes["purchasing_habits"] = habits
        return self

    def brand_loyalty(self, loyalty: List[str]):
        self.attributes["brand_loyalty"] = loyalty
        return self

    def product_usage(self, usage: List[str]):
        self.attributes["product_usage"] = usage
        return self

    def media_consumption(self, media: List[str]):
        self.attributes["media_consumption"] = media
        return self

    def device_usage(self, devices: List[str]):
        self.attributes["device_usage"] = devices
        return self

    def platform_preferences(self, platforms: List[str]):
        self.attributes["platform_preferences"] = platforms
        return self

    def digital_media_interaction(self, level: str):
        self.attributes["digital_media_interaction"] = level
        return self

    def location_context(self, context: List[str]):
        self.attributes["location_context"] = context
        return self

    def cultural_influences(self, cultures: List[str]):
        self.attributes["cultural_influences"] = cultures
        return self

    def data_integration_tools(self, tools: List[str]):
        self.attributes["data_integration_tools"] = tools
        return self

    def data_collection_consent(self, consented: bool):
        self.attributes["data_collection_consent"] = consented
        return self

    def anonymize_data(self, anonymize: bool):
        self.attributes["anonymize_data"] = anonymize
        return self

    def add_trait(self, trait_name: str, trait_value: Any):
        self.attributes[trait_name] = trait_value
        return self

    def describe(self) -> str:
        description_lines = [f"Target Audience ID: {self.id}"]
        for attribute, value in self.attributes.items():
            description_lines.append(f"{attribute.capitalize()}: {value}")
        return "\n".join(description_lines)

    async def spawn_agents(self, num_agents: int) -> List[any]:
        cognitive_model = OpenAILanguageModel(
            model_id=CognitiveModel.GPT_4, agent_id=self.id
        )

        tasks = []
        for _ in range(num_agents):
            task = asyncio.create_task(
                spawn_agent(
                    cognitive_model,
                    self.cognitive_model_id,
                    list(self.attributes.items()),
                )
            )
            tasks.append(task)

        self.agents = await asyncio.gather(*tasks)

        return self.agents

    async def run_conversation_test(
        self, questions: List[str], iterations: int
    ) -> List[any]:
        spawn_task = None
        if len(self.agents) < iterations:
            spawn_task = asyncio.create_task(
                self.spawn_agents(iterations - len(self.agents))
            )

        # Wait for the spawn task if it was started
        if spawn_task:
            await spawn_task

        # Prepare and run ask tasks for all agents and questions
        responses = []
        for agent in self.agents:
            for question in questions:
                print(f"Agent {agent.id} asked: {question}")
                response = await agent.ask(question)
                print(f"Agent {agent.id} responded: {response}")
                responses.append(response)

                yield response
