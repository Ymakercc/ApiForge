from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, JSON, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Interface(Base):
    __tablename__ = "interfaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    method: Mapped[str] = mapped_column(
        Enum("GET", "POST", "PUT", "PATCH", "DELETE", name="http_method"), nullable=False
    )
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    headers: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    params: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    body: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    auth_type: Mapped[str] = mapped_column(
        Enum("none", "bearer", "basic", "apikey", name="auth_type"),
        nullable=False,
        default="none",
    )
    auth_config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    is_enabled: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, index=True)
    created_by: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
