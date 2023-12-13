import time
from http import HTTPStatus

from tests.integration.api_test_tools import ApiTestTools


class TestPlayerApi:
    def test_get_player_no_player_exists(self):
        username = f'nonexistent_{str(time.time())}'

        response = ApiTestTools.get_player(username)

        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        assert response_json == {}

    def test_create_player_successful(self):
        username = f'test_creation_{str(time.time())}'

        response = ApiTestTools.create_player(username)

        assert response.status_code == HTTPStatus.OK

        response_json = response.json()
        assert response_json['points'] == 0
        assert response_json['coins'] == 0
        assert response_json['spins'] == 100
        assert response_json['current_mission_index'] == 1
        assert response_json['accumulated_points_towards_goal'] == 0

        get_response = ApiTestTools.get_player(username)

        assert get_response.status_code == HTTPStatus.OK
        get_response_json = get_response.json()
        assert get_response_json['username'] == username

    def test_create_player_with_invalid_name_fails(self):
        too_short = 'a'
        too_long = 'a' * 150
        invalid_chars = '*&@$!'
        invalid_names = [too_short, too_long, invalid_chars]
        for username in invalid_names:
            response = ApiTestTools.create_player(username)

            assert response.status_code == HTTPStatus.BAD_REQUEST
