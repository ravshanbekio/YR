from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.connection import Base

class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.chat_id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    text_answer: Mapped[str] = mapped_column(String(255), nullable=True)
    file_answer: Mapped[str] = mapped_column(String(255), nullable=True)
    # Relationships
    question = relationship("Question", primaryjoin="Question.id==Answer.question_id", back_populates="answer")

    def __str__(self):
        return f"Answer({self.id})"