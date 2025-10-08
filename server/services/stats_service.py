from sqlalchemy.orm import Session
from ..models import UserStat

class StatsService:
    def __init__(self, db: Session):
        self.db = db

    def add_upload(self, user_id: int, bytes_up: int):
        st = self.db.query(UserStat).filter_by(user_id=user_id).first()
        if not st:
            st = UserStat(user_id=user_id)
            self.db.add(st)
        st.bytes_up += int(bytes_up)
        return st

    def add_download(self, user_id: int, bytes_down: int):
        st = self.db.query(UserStat).filter_by(user_id=user_id).first()
        if not st:
            st = UserStat(user_id=user_id)
            self.db.add(st)
        st.bytes_down += int(bytes_down)
        return st