from typing import Optional

from pydantic import BaseModel

from models.player import Player


class CreatePlayerRequest(BaseModel):
    username: str


class PlayerResponse(BaseModel):
    player: Optional[Player] = None
