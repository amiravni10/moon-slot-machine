from managers.db_manager import DbManager
from models.session import Session


class SessionManager:
    @classmethod
    def get_session(cls) -> Session:
        db_session = DbManager.get_redis_session()
        session = Session(db_session=db_session)
        return session
