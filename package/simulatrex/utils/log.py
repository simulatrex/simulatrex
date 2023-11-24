"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: log_config.py
Description: Log helper

"""
import logging
import json

from termcolor import colored


class Logger:
    def __init__(
        self,
        name="simulatrex::simulation",
        log_file="simulatrex_logs.log",
        agent_log_file="simulatrex_agent_logs.log",
    ):
        # Create logger
        self.logger = logging.getLogger(name)
        self.agent_logger = logging.getLogger("agent_logger")

        if not self.logger.handlers:  # Check if logger already has handlers
            self.logger.setLevel(logging.DEBUG)  # Set default logging level

            # Create formatter
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            # Create console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

            # Create file handler and set level to debug
            if log_file is not None:
                fh = logging.FileHandler(log_file)
                fh.setLevel(logging.DEBUG)
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)

        if not self.agent_logger.handlers:  # Check if logger already has handlers
            self.agent_logger.setLevel(logging.INFO)
            # Create file handler for agent response log
            if agent_log_file is not None:
                rh = logging.FileHandler(agent_log_file)
                rh.setLevel(logging.INFO)
                rh.setFormatter(formatter)
                self.agent_logger.addHandler(rh)

    def debug(self, msg):
        self.logger.debug(colored(msg, "blue"))

    def info(self, msg):
        self.logger.info(colored(msg, "green"))

    def warning(self, msg):
        self.logger.warning(colored(msg, "yellow"))

    def error(self, msg):
        self.logger.error(colored(msg, "red"))

    def log_agent_response(self, agent_id: str, response: str):
        self.agent_logger.info(f"{agent_id} - {response}")


SingletonLogger = Logger()
