from typing import Optional

from redis.asyncio.lock import Lock

from models.errors import PlayerAlreadyExistsException
from models.player import Player
from models.session import Session


class PlayerRepository:
    PLAYER_KEY_PREFIX = 'player:'
    LOCK_TIMEOUT = 10
    BLOCKING_TIMEOUT = 10

    @classmethod
    def __generate_player_key(cls, username: str) -> str:
        return f'{cls.PLAYER_KEY_PREFIX}{username}'

    @classmethod
    async def get_player(cls, session: Session, username: str) -> Optional[Player]:
        player_key = cls.__generate_player_key(username)
        player_json = await session.db_session.get(player_key)
        if not player_json:
            return None
        return Player.model_validate_json(player_json)

    @classmethod
    def __generate_lock_key(cls, username: str) -> str:
        return f'{cls.PLAYER_KEY_PREFIX}{username}:LOCK'

    @classmethod
    async def create_player(cls, session: Session, username: str) -> Player:
        existing_player = await cls.get_player(session, username)
        if existing_player:
            raise PlayerAlreadyExistsException(f'Player with username: {username} already exists')
        new_player = Player(username=username)
        await cls.__set_player(session, new_player)
        return new_player

    @classmethod
    async def __set_player(cls, session: Session, player: Player):
        player_key = cls.__generate_player_key(player.username)
        await session.db_session.set(player_key, player.model_dump_json())

    @classmethod
    async def update_player(cls, session: Session, player: Player):
        await cls.__set_player(session, player)

    @classmethod
    async def lock(cls, session: Session, username: str) -> Lock:
        lock_key = cls.__generate_lock_key(username)
        lock = session.db_session.lock(lock_key, timeout=cls.LOCK_TIMEOUT, blocking_timeout=cls.BLOCKING_TIMEOUT)
        acquired = await lock.acquire()
        if not acquired:
            raise Exception(f'Could not acquire a lock!')
        return lock
