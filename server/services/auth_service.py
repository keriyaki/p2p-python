from sqlalchemy.orm import Session
from ..models import User, Role, UserStat
from ..security import verify_password, create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, username: str, password: str) -> str | None:
        user = self.db.query(User).filter(User.username == username, User.is_banned == False).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return create_access_token(str(user.id))