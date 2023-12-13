from typing import List, Optional

from pydantic import BaseModel


class SpinRequest(BaseModel):
    username: str


class SpinResponse(BaseModel):
    result: List[int]
    points_earned: int = 0
    spins_earned: int = 0
    coins_earned: int = 0
    points_balance: Optional[int] = None
    spins_balance: Optional[int] = None
    coins_balance: Optional[int] = None
