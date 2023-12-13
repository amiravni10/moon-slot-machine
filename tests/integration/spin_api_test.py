import time
from http import HTTPStatus

from tests.integration.api_test_tools import ApiTestTools


class TestApinApi:
    def test_new_player_spins(self):
        username = f'test_spin_{str(time.time())}'
        create_response = ApiTestTools.create_player(username)
        assert create_response.status_code == HTTPStatus.OK
        get_response = ApiTestTools.get_player(username)
        assert get_response.status_code == HTTPStatus.OK
        get_response_json = get_response.json()
        current_spins = get_response_json['player']['spins']

        spin_response = ApiTestTools.spin(username)

        assert spin_response.status_code == HTTPStatus.OK
        spin_response_json = spin_response.json()
        assert spin_response_json['spins_balance'] == current_spins - 1
        spin_result = spin_response_json['result']
        assert len(spin_result) == 3
