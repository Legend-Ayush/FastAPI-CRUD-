from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class User(Base):
    __tablename__ = 'customer'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hash_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), #handles timezone-aware datetime values
        default=lambda: datetime.now(timezone.utc)
    )
    
    is_deleted:Mapped[bool] = mapped_column(Boolean, default=False)
    schedule_delete_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)