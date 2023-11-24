"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: prompts.py
Description: Prompt Templates
Prompt Templates are used to generate prompts for the LLM.

"""
from enum import Enum
import os


class TemplateType(Enum):
    AGENT_IDENTITY_SPAWN = "agent_identity_spawn.txt"
    AGENT_PERCEPTION = "agent_perception.txt"
    AGENT_CONVERSE = "agent_converse.txt"
    AGENT_THINK = "agent_think.txt"
    AGENT_EVALUATION = "agent_evaluation.txt"
    AGENT_DECIDE_ON_CONVERSATION = "agent_decide_on_conversation.txt"
    AGENT_START_CONVERSATION = "agent_start_conversation.txt"
    AGENT_REPLY_TO_CONVERSATION = "agent_reply_to_conversation.txt"
    SUMMARIZE_ENVIRONMENT = "summarize_environment.txt"
    EVALUATE_AGENT_OUTPUTS = "evaluate_agent_outputs.txt"
    AGENT_INTERVIEW = "agent_interview.txt"


class PromptManager:
    def __init__(self, template_dir="prompt_templates"):
        self.template_dir = template_dir
        self.templates = self._load_templates()

    def _load_templates(self):
        templates = {}
        for template_type in TemplateType:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_dir_path = os.path.join(current_dir, self.template_dir)
            with open(os.path.join(template_dir_path, template_type.value), "r") as f:
                templates[template_type] = f.read()
        return templates

    def get_filled_template(self, template_type: TemplateType, **attributes) -> str:
        if template_type not in self.templates:
            raise ValueError(f"Template type {template_type} not found!")

        return self.templates[template_type].format(**attributes)
