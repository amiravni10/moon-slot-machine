import re
from typing import Optional

from models.errors import InvalidPlayerNameException


class PlayerManager:
    MIN_USERNAME_LENGTH = 2
    MAX_USERNAME_LENGTH = 100
    USERNAME_VALIDATION_REGEX = re.compile(r'^[a-zA-Z0-9_@.-]+$')

    @classmethod
    def validate_username(cls, username: Optional[str]):
        if not username:
            raise InvalidPlayerNameException('Username cannot be empty')
        if len(username) < cls.MIN_USERNAME_LENGTH:
            raise InvalidPlayerNameException(f'Username length must not be less than: {cls.MIN_USERNAME_LENGTH}')
        if len(username) > cls.MAX_USERNAME_LENGTH:
            raise InvalidPlayerNameException(f'Username length must not be greater than: {cls.MAX_USERNAME_LENGTH}')
        if not cls.USERNAME_VALIDATION_REGEX.match(username):
            raise InvalidPlayerNameException(
                f'Username must only contain letters, numbers and the following chars: (_, @, ., -)')
