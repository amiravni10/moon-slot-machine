import json

from models.configuration import GoalsConfig


class ConfigManager:
    @classmethod
    def get_system_config(cls) -> dict:
        with open('system_config.json') as system_config_file:
            system_config = json.load(system_config_file)
            return system_config

    @classmethod
    def get_goals_config(cls) -> GoalsConfig:
        with open('goals_config.json') as goals_config_file:
            goals_config_json = json.load(goals_config_file)
            goals_config = GoalsConfig.model_validate(goals_config_json)
            return goals_config
