import random
from typing import List

from api.spin_api import SpinRequest, SpinResponse
from managers.config_manager import ConfigManager
from managers.goals_manager import GoalsManager
from models.errors import PlayerDoesNotExistException, PlayerHasNoSpinBalanceException
from models.player import Player
from models.session import Session
from repositories.player_repository import PlayerRepository


class SpinManager:
    @classmethod
    def __generate_slot_machine_result(cls) -> List[int]:
        return [random.randint(0, 9) for _ in range(3)]

    @classmethod
    async def __spin_core(cls, player: Player) -> SpinResponse:
        if not player:
            raise PlayerDoesNotExistException()
        if player.spins <= 0:
            raise PlayerHasNoSpinBalanceException()
        player.spins -= 1
        result = cls.__generate_slot_machine_result()
        spin_result = SpinResponse(result=result)
        if all(element == result[0] for element in result):
            points_earned = sum(result)
            spin_result.points_earned = points_earned
            player.points += points_earned
            goals_config = ConfigManager.get_goals_config()
            process_result = GoalsManager.process_goals(player, points_earned, goals_config)
            spin_result.spins_earned = process_result.total_spins_earned
            player.spins += process_result.total_spins_earned
            spin_result.coins_earned = process_result.total_coins_earned
            player.coins += process_result.total_coins_earned
            player.accumulated_points_towards_goal = process_result.accumulated_points_towards_next_goal
            player.current_mission_index = process_result.current_mission_index

        spin_result.points_balance = player.points
        spin_result.spins_balance = player.spins
        spin_result.coins_balance = player.coins
        return spin_result

    @classmethod
    async def spin(cls, session: Session, spin_request: SpinRequest) -> SpinResponse:
        lock = await PlayerRepository.lock(session, spin_request.username)
        try:
            player = await PlayerRepository.get_player(session, spin_request.username)
            spin_result = await cls.__spin_core(player)
            await PlayerRepository.update_player(session, player)
            return spin_result
        finally:
            await lock.release()
