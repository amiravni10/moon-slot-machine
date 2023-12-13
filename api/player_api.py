from pydantic import BaseModel


class CreatePlayerRequest(BaseModel):
    username: str
