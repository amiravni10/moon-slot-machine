from typing import List, Optional

from pydantic import BaseModel, Field


class ProcessGoalsResult(BaseModel):
    goals_achieved: List[int] = Field(default_factory=list, description='List of indexes of achieved goals')
    total_coins_earned: int = 0
    total_spins_earned: int = 0
    current_mission_index: Optional[int] = None
    accumulated_points_towards_next_goal: int = 0
