import os

import requests
from requests import Response


class ApiTestTools:
    HOST = os.getenv('HOST_URL', 'localhost')
    PORT = int(os.getenv('HOST_PORT', '8000'))
    SCHEMA = os.getenv('HOST_SCHEMA', 'http')
    PLAYER_API = 'player'
    SPIN_API = 'spin'

    @classmethod
    def get_host_url(cls) -> str:
        return f'{cls.SCHEMA}://{cls.HOST}:{cls.PORT}'

    @classmethod
    def get_player(cls, username: str) -> Response:
        host_url = ApiTestTools.get_host_url()
        full_url = f'{host_url}/{cls.PLAYER_API}/{username}'
        response = requests.get(full_url)
        return response

    @classmethod
    def create_player(cls, username: str) -> Response:
        host_url = ApiTestTools.get_host_url()
        full_url = f'{host_url}/{cls.PLAYER_API}'
        request = {
            'username': username
        }
        response = requests.post(full_url, json=request)
        return response

    @classmethod
    def spin(cls, username: str) -> Response:
        host_url = ApiTestTools.get_host_url()
        full_url = f'{host_url}/{cls.SPIN_API}'
        request = {
            'username': username
        }
        response = requests.post(full_url, json=request)
        return response
