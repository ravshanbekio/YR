from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from db.connection import Base
from api.models.mtm import user_vacancy_mtm

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[str] = mapped_column(String(100), unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(13), nullable=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime)
    # Relationships
    vacancy = relationship("Vacancy", secondary=user_vacancy_mtm, cascade="all", back_populates="user")

    def __str__(self):
        return f"{self.full_name} - {self.chat_id}"