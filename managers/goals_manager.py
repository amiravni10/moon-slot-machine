from models.configuration import GoalsConfig
from models.goals import ProcessGoalsResult
from models.player import Player


class GoalsManager:
    @classmethod
    def process_goals(cls, player: Player, points_earned: int, goals_config: GoalsConfig) -> ProcessGoalsResult:
        result = ProcessGoalsResult()
        mission_index = player.current_mission_index
        total_points = player.accumulated_points_towards_goal + points_earned
        while total_points:
            current_goal = goals_config.missions[mission_index - 1]
            if not total_points >= current_goal.points_goal:
                result.accumulated_points_towards_next_goal = total_points
                break
            result.goals_achieved.append(mission_index)
            for reward in current_goal.rewards:
                reward_name = reward.name
                if reward_name == 'coins':
                    result.total_coins_earned += reward.value
                elif reward_name == 'spins':
                    result.total_spins_earned += reward.value

            total_points -= current_goal.points_goal
            if mission_index >= len(goals_config.missions):
                mission_index = goals_config.repeated_index
            else:
                mission_index = mission_index + 1
        result.current_mission_index = mission_index
        return result
