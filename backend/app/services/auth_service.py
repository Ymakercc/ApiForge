from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.models.user import User


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user


def create_token_for_user(user: User) -> str:
    return create_access_token({"sub": str(user.id), "username": user.username, "role": user.role})
