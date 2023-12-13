from typing import Optional, List

from pydantic import BaseModel


class RedisConfig(BaseModel):
    host: str
    port: int
    password: Optional[str] = None


class RewardConfig(BaseModel):
    name: str
    value: int


class MissionConfig(BaseModel):
    rewards: List[RewardConfig]
    points_goal: int


class GoalsConfig(BaseModel):
    missions: List[MissionConfig]
    repeated_index: int
