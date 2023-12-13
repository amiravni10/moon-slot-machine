from pydantic import BaseModel, Field


class Player(BaseModel):
    username: str
    spins: int = Field(default=100, description='The spin balance')
    points: int = Field(default=0, description='Total points accumulated alltime')
    coins: int = Field(default=0, description='Total coins earned')
    current_mission_index: int = Field(default=1,
                                       description='Keeps track of the current mission by index from config')
    accumulated_points_towards_goal: int = Field(default=0,
                                                 description='Keeps track of the amount of points accumulated '
                                                             'towards next completion')
