"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: engine.py
Description: Main engine for running simulations

"""
from typing import List

from simulatrex.config import Config
from simulatrex.agent import LLMAgent
from simulatrex.environment import (
    StaticEnvironment,
    DynamicEnvironment,
    EnvironmentType,
)
from simulatrex.evaluation import EvaluationEngine
from simulatrex.target_group import TargetGroup
from simulatrex.utils.json_utils import JSONHelper
from simulatrex.utils.log import SingletonLogger

_logger = SingletonLogger


class SimulationEngine:
    def __init__(self, config_path: str):
        json_data = JSONHelper.read_json(config_path)
        self.config = Config(**json_data)
        self.title = self.config.simulation.title

        self.environment = self.init_environment()

        time_config = self.config.simulation.environment.time_config
        self.environment.init_time(time_config)

        self.current_iteration = 1
        self.total_iterations = (
            self.environment.end_time - self.environment.start_time
        ) / self.environment.time_multiplier

    async def init_target_groups(self) -> List[LLMAgent]:
        agents = []

        for group in self.config.simulation.target_groups:
            target_group = TargetGroup(
                group.id,
                group.role,
                group.responsibilities,
                group.initial_conditions,
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
                await agent.initiate_conversation(self.environment)

                # Agent perceives the recent events
                for event in recent_events:
                    _logger.debug(f"Event - ID: {event.id}, Content: {event.content}")
                    await agent.perceive_event(
                        event,
                        self.environment,
                    )
                    await agent._process_messages()

            # Log the current iteration
            _logger.info(
                f"Simulation Iteration {self.current_iteration} of {self.total_iterations}: Processed recent events."
            )

            self.current_iteration += 1

        # Evaluate the simulation
        _logger.info("Simulation finished. Evaluating results...")
        evaluation_engine = EvaluationEngine(self.config.simulation.evaluation)
        simulation_results = await evaluation_engine.evaluate_agents_outputs(
            self.agents, self.environment
        )
        _logger.info(f"Simulation results: {simulation_results}")
