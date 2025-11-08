from sqlalchemy import Integer, String, Enum, Boolean, ForeignKey, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign, remote

from db.connection import Base
from api.schemas.questions import QuestionTypeEnum

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"))
    title: Mapped[str] = mapped_column(String(255))
    question_type: Mapped[QuestionTypeEnum] = mapped_column(Enum(QuestionTypeEnum), default=QuestionTypeEnum.TEXT, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
    # Relationships
    vacancy = relationship("Vacancy", back_populates="questions")
    answer = relationship("Answer", back_populates="question", uselist=False)

    def __str__(self):  
        return f"{self.title}"