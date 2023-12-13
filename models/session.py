from redis.asyncio import StrictRedis


class Session:
    def __init__(self, db_session: StrictRedis):
        self.db_session = db_session
