import logging
from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, Depends, HTTPException

from api.player_api import CreatePlayerRequest
from api.spin_api import SpinRequest
from managers.config_manager import ConfigManager
from managers.db_manager import DbManager
from managers.player_manager import PlayerManager
from managers.session_manager import SessionManager
from managers.spin_manager import SpinManager
from models.errors import PlayerAlreadyExistsException, PlayerDoesNotExistException, PlayerHasNoSpinBalanceException, \
    InvalidPlayerNameException
from models.session import Session
from repositories.player_repository import PlayerRepository

logging.basicConfig(level=logging.INFO)
system_config = ConfigManager.get_system_config()
DbManager.init(system_config)
app = FastAPI()


def validate_username(username: str):
    try:
        PlayerManager.validate_username(username)
    except InvalidPlayerNameException:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Invalid username provided')


@app.get("/player/{username}")
async def get_player(username: str, session: Session = Depends(SessionManager.get_session)):
    validate_username(username)
    player = await PlayerRepository.get_player(session, username)
    if not player:
        return {}
    return player


@app.post("/player")
async def create_player(create_player_request: CreatePlayerRequest,
                        session: Session = Depends(SessionManager.get_session)):
    validate_username(create_player_request.username)
    try:
        created_player = await PlayerRepository.create_player(session, create_player_request.username)
    except PlayerAlreadyExistsException:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Username already exists')
    return created_player


@app.post('/spin')
async def spin(spin_request: SpinRequest, session: Session = Depends(SessionManager.get_session)):
    validate_username(spin_request.username)
    try:
        spin_result = await SpinManager.spin(session, spin_request)
        return spin_result
    except PlayerDoesNotExistException:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Player {spin_request.username} not found')
    except PlayerHasNoSpinBalanceException:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                            detail=f'Player {spin_request.username} has no spin balance remaining')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
