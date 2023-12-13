from typing import Optional

from redis.asyncio import StrictRedis

from models.configuration import RedisConfig


class DbManager:
    app_redis_config: Optional[RedisConfig] = None

    @classmethod
    def init(cls, system_config: dict):
        cls.app_redis_config = RedisConfig.model_validate(system_config['redis_config'])

    @classmethod
    def get_redis_session(cls) -> StrictRedis:
        redis = StrictRedis(host=cls.app_redis_config.host, port=cls.app_redis_config.port,
                            password=cls.app_redis_config.password, decode_responses=True)
        return redis
