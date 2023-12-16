"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: engine.py
Description: Main engine for running simulations

"""
import re
import pandas as pd
from typing import List

from simulatrex.experiments.possibleworlds.config import Config
from simulatrex.agent.agent import LLMAgent
from simulatrex.experiments.possibleworlds.environment import (
    StaticEnvironment,
    DynamicEnvironment,
    EnvironmentType,
)
from simulatrex.experiments.possibleworlds.evaluation import EvaluationEngine
from simulatrex.experiments.possibleworlds.target_group import (
    TargetGroup,
    TargetGroupRelationship,
)
from simulatrex.utils.json_utils import JSONHelper
from simulatrex.utils.log import SingletonLogger

_logger = SingletonLogger


class SimulationEngine:
    def __init__(
        self,
        config_path: str = None,
        config: dict = None,
    ):
        _logger.info("Initializing simulation engine...")
        if config_path:
            json_data = JSONHelper.read_json(config_path)
        elif config:
            json_data = config
        else:
            raise ValueError("Either config_path or config must be provided")
        self.config = Config(**json_data)
        self.title = self.config.simulation.title

        self.environment = self.init_environment()

        time_config = self.config.simulation.environment.time_config
        self.environment.init_time(time_config)

        self.current_iteration = 1
        self.total_iterations = (
            self.environment.end_time - self.environment.start_time
        ) / self.environment.time_multiplier

        self.simulation_results = None

    async def init_target_groups(self) -> List[LLMAgent]:
        agents = []

        _target_groups = self.config.simulation.target_groups
        for group in _target_groups:
            relationships: List[TargetGroupRelationship] = []
            if group.relationships:
                for relationship in group.relationships:
                    if relationship.target_group_id not in [
                        group.id for group in self.config.simulation.target_groups
                    ]:
                        raise ValueError(
                            f"Referred target group {relationship.target_group_name} does not exist"
                        )

                    # Create a new target group relationship
                    _target_group_relation_role = next(
                        (
                            target_group.role
                            for target_group in _target_groups
                            if target_group.id == relationship.target_group_id
                        ),
                        None,
                    )

                    _target_group_relation = TargetGroupRelationship(
                        _target_group_relation_role,
                        relationship.type,
                        relationship.strength,
                    )

                    relationships.append(_target_group_relation)
            else:
                _logger.info(f"No relationships defined for target group {group.id}.")

            # Create a new target group
            target_group = TargetGroup(
                group.id,
                group.role,
                group.responsibilities,
                group.initial_conditions,
                relationships,
            )
            target_agents = await target_group.spawn_agents(group.num_agents)

            agents.extend(target_agents)

        return agents

    def init_agents(self) -> List[LLMAgent]:
        agents = []

        for agent in self.config.simulation.agents:
            new_agent = LLMAgent(
                agent.id,
                agent.type,
                agent.identity,
                agent.initial_conditions,
                agent.cognitive_model,
                agent.relationships,
                agent.group_affiliations,
            )

            agents.append(new_agent)

        return agents

    def init_environment(self):
        environment_settings = self.config.simulation.environment
        enviroment_type = environment_settings.type
        events = self.config.simulation.events

        if enviroment_type == EnvironmentType.Static.value:
            new_environment = StaticEnvironment(
                environment_settings.description,
                environment_settings.context,
                environment_settings.entities,
                events,
            )
            return new_environment
        elif enviroment_type == EnvironmentType.Dynamic.value:
            new_environment = DynamicEnvironment(
                environment_settings.description,
                environment_settings.context,
                environment_settings.entities,
                events,
            )
            return new_environment
        else:
            raise ValueError(f"Unsupported environment type: {enviroment_type}")

    def add_message_for_agent(self, agent_id: str, message):
        try:
            agent = next(
                agent
                for agent in self.agents
                if re.search(rf"\b{re.escape(agent.id)}\b", agent_id)
            )
            agent.message_queue.append(message)
        except StopIteration:
            _logger.error(f"Agent with ID {agent_id} not found")

    async def run(self):
        # Initialize agents
        if self.config.simulation.target_groups is not None:
            self.agents = await self.init_target_groups()
        else:
            self.agents = self.init_agents()

        while True:
            # Check stopping time
            if not self.environment.is_running():
                break

            # Update the environment
            recent_events, current_env_context = await self.environment.update()

            # Log the current env context
            _logger.debug(f"Current environment context: {current_env_context}")

            # Let the agents process the recent events
            for agent in self.agents:
                # Agent thinks about environment context
                await agent.think(self.environment)
                await agent.initiate_conversation(
                    self.environment, self.add_message_for_agent
                )
                await agent._process_messages(self.add_message_for_agent)

                # Agent perceives the recent events
                for event in recent_events:
                    _logger.debug(f"Event - ID: {event.id}, Content: {event.content}")
                    await agent.perceive_event(
                        event,
                        self.environment,
                    )

            # Log the current iteration
            _logger.info(
                f"Simulation Iteration {self.current_iteration} of {self.total_iterations}: Processed recent events."
            )

            self.current_iteration += 1

        # Evaluate the simulation
        _logger.info("Simulation finished. Evaluating results...")
        evaluation_engine = EvaluationEngine(self.config.simulation.evaluation)
        self.simulation_results = await evaluation_engine.evaluate_agents_outputs(
            self.agents, self.environment
        )
        _logger.info(f"Simulation results: {self.simulation_results}")

    def get_evaluation_data(self):
        data = []
        for result in self.simulation_results:
            data.append(
                {
                    "objective_id": result["objective_id"],
                    "description": result["description"],
                    "llm_response": result["llm_response"],
                }
            )
        return pd.DataFrame(data)
