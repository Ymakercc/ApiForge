from datetime import datetime
from sqlalchemy import DateTime, Integer, JSON, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class SkillTemplate(Base):
    __tablename__ = "skill_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    template_content: Mapped[str] = mapped_column(Text, nullable=False)
    variables: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    is_active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
