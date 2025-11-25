from sqlalchemy import Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from db.connection import Base
from api.models.mtm import user_vacancy_mtm

class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    # Relationships
    questions = relationship("Question", back_populates="vacancy")
    user = relationship("User", secondary=user_vacancy_mtm, back_populates="vacancy")
    
    def __str__(self):
        return f"{self.title}"