from managers.goals_manager import GoalsManager
from models.configuration import GoalsConfig
from models.player import Player

TEST_GOALS_CONFIG = {
    "missions": [
        {
            "rewards": [
                {
                    "name": "spins",
                    "value": 10
                }
            ],
            "points_goal": 10
        },
        {
            "rewards": [
                {
                    "name": "coins",
                    "value": 10
                }
            ],
            "points_goal": 20
        },
        {
            "rewards": [
                {
                    "name": "coins",
                    "value": 100
                },
                {
                    "name": "spins",
                    "value": 100
                }
            ],
            "points_goal": 100
        }
    ],
    "repeated_index": 1
}


class TestGoalsManager:
    def test_process_goals_first_time_no_goal_achieved(self):
        username = 'test_user'
        player = Player(username=username)
        player.spins = 5
        goals_config = GoalsConfig.model_validate(TEST_GOALS_CONFIG)
        points_earned = 6

        process_result = GoalsManager.process_goals(player, points_earned, goals_config)

        assert not process_result.goals_achieved
        assert process_result.total_spins_earned == 0
        assert process_result.total_coins_earned == 0
        assert process_result.current_mission_index == player.current_mission_index
        assert process_result.accumulated_points_towards_next_goal == points_earned

    def test_process_goals_first_time_points_midway_goal_achieved(self):
        username = 'test_user'
        player = Player(username=username)
        player.spins = 5
        player.accumulated_points_towards_goal = 6
        goals_config: GoalsConfig = GoalsConfig.model_validate(TEST_GOALS_CONFIG)
        points_earned = 6

        process_result = GoalsManager.process_goals(player, points_earned, goals_config)

        assert len(process_result.goals_achieved) == 1
        assert 1 in process_result.goals_achieved
        assert process_result.total_spins_earned == 10
        assert process_result.total_coins_earned == 0
        assert process_result.current_mission_index == player.current_mission_index + 1
        assert process_result.accumulated_points_towards_next_goal == (
                points_earned + player.accumulated_points_towards_goal) - 10

    def test_process_goals_first_time_first_goal_achieved(self):
        username = 'test_user'
        player = Player(username=username)
        player.spins = 5
        goals_config = GoalsConfig.model_validate(TEST_GOALS_CONFIG)
        points_earned = 11

        process_result = GoalsManager.process_goals(player, points_earned, goals_config)

        assert len(process_result.goals_achieved) == 1
        assert 1 in process_result.goals_achieved
        assert process_result.total_spins_earned == 10
        assert process_result.total_coins_earned == 0
        assert process_result.current_mission_index == player.current_mission_index + 1
        assert process_result.accumulated_points_towards_next_goal == (
                points_earned + player.accumulated_points_towards_goal) - 10

    def test_process_goals_first_time_two_goals_achieved(self):
        username = 'test_user'
        player = Player(username=username)
        player.spins = 5
        goals_config = GoalsConfig.model_validate(TEST_GOALS_CONFIG)
        points_earned = 31

        process_result = GoalsManager.process_goals(player, points_earned, goals_config)

        assert len(process_result.goals_achieved) == 2
        assert 1 in process_result.goals_achieved
        assert 2 in process_result.goals_achieved
        assert process_result.total_spins_earned == 10
        assert process_result.total_coins_earned == 10
        assert process_result.current_mission_index == player.current_mission_index + 2
        assert process_result.accumulated_points_towards_next_goal == (
                points_earned + player.accumulated_points_towards_goal) - 30

    def test_process_goals_first_time_more_than_one_full_cycle_achieved(self):
        username = 'test_user'
        player = Player(username=username)
        player.spins = 5
        goals_config = GoalsConfig.model_validate(TEST_GOALS_CONFIG)
        points_earned = 170

        process_result = GoalsManager.process_goals(player, points_earned, goals_config)

        assert len(process_result.goals_achieved) == 5
        all_ones = [g for g in process_result.goals_achieved if g == 1]
        assert len(all_ones) == 2
        all_twos = [g for g in process_result.goals_achieved if g == 2]
        assert len(all_twos) == 2
        all_threes = [g for g in process_result.goals_achieved if g == 3]
        assert len(all_threes) == 1
        assert process_result.total_spins_earned == 120
        assert process_result.total_coins_earned == 120
        assert process_result.current_mission_index == 3
        assert process_result.accumulated_points_towards_next_goal == 10

    def test_process_goals_goals_achieved_and_now_additional_goal_achieved(self):
        username = 'test_user'
        player = Player(username=username)
        player.spins = 5
        goals_config = GoalsConfig.model_validate(TEST_GOALS_CONFIG)
        points_earned = 11
        player.accumulated_points_towards_goal = 15
        player.current_mission_index = 2

        process_result = GoalsManager.process_goals(player, points_earned, goals_config)

        assert len(process_result.goals_achieved) == 1
        assert 2 in process_result.goals_achieved
        assert process_result.total_spins_earned == 0
        assert process_result.total_coins_earned == 10
        assert process_result.current_mission_index == player.current_mission_index + 1
        assert process_result.accumulated_points_towards_next_goal == (
                points_earned + player.accumulated_points_towards_goal) - 20

    def test_process_goals_goals_achieved_and_now_additional_multiple_goals_achieved(self):
        username = 'test_user'
        player = Player(username=username)
        player.spins = 5
        goals_config = GoalsConfig.model_validate(TEST_GOALS_CONFIG)
        points_earned = 320
        player.accumulated_points_towards_goal = 15
        player.current_mission_index = 2

        process_result = GoalsManager.process_goals(player, points_earned, goals_config)

        assert len(process_result.goals_achieved) == 7
        all_ones = [g for g in process_result.goals_achieved if g == 1]
        assert len(all_ones) == 2
        all_twos = [g for g in process_result.goals_achieved if g == 2]
        assert len(all_twos) == 3
        all_threes = [g for g in process_result.goals_achieved if g == 3]
        assert len(all_threes) == 2
        assert process_result.total_spins_earned == 220
        assert process_result.total_coins_earned == 230
        assert process_result.current_mission_index == 3
        assert process_result.accumulated_points_towards_next_goal == 55

    def test_process_goals_exact_point_match(self):
        username = 'test_user'
        player = Player(username=username)
        player.spins = 5
        player.accumulated_points_towards_goal = 6
        goals_config: GoalsConfig = GoalsConfig.model_validate(TEST_GOALS_CONFIG)
        points_earned = 4

        process_result = GoalsManager.process_goals(player, points_earned, goals_config)

        assert len(process_result.goals_achieved) == 1
        assert 1 in process_result.goals_achieved
        assert process_result.total_spins_earned == 10
        assert process_result.total_coins_earned == 0
        assert process_result.current_mission_index == player.current_mission_index + 1
        assert process_result.accumulated_points_towards_next_goal == (
                points_earned + player.accumulated_points_towards_goal) - 10

    def test_process_goals_first_time_more_than_one_full_cycle_achieved_and_repeated_index_is_not_one(self):
        username = 'test_user'
        player = Player(username=username)
        player.spins = 5
        goals_config: GoalsConfig = GoalsConfig.model_validate(TEST_GOALS_CONFIG)
        goals_config.repeated_index = 2
        points_earned = 170

        process_result = GoalsManager.process_goals(player, points_earned, goals_config)

        assert len(process_result.goals_achieved) == 4
        all_ones = [g for g in process_result.goals_achieved if g == 1]
        assert len(all_ones) == 1
        all_twos = [g for g in process_result.goals_achieved if g == 2]
        assert len(all_twos) == 2
        all_threes = [g for g in process_result.goals_achieved if g == 3]
        assert len(all_threes) == 1
        assert process_result.total_spins_earned == 110
        assert process_result.total_coins_earned == 120
        assert process_result.current_mission_index == 3
        assert process_result.accumulated_points_towards_next_goal == 20
