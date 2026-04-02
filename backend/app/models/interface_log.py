from datetime import datetime
from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, JSON, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class InterfaceLog(Base):
    __tablename__ = "interface_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    interface_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("interfaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    request_method: Mapped[str] = mapped_column(String(16), nullable=False)
    request_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    request_headers: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    request_body: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    response_status: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    response_body: Mapped[str | None] = mapped_column(Text, nullable=True)
    response_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_success: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, index=True)
    error_message: Mapped[str | None] = mapped_column(String(512), nullable=True)
    triggered_by: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )
