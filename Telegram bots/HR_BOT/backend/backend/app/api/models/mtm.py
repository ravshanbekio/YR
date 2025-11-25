from sqlalchemy import Table, Column, ForeignKey, DateTime, func

from db.connection import Base

user_vacancy_mtm = Table(
    "user_vacancy",
    Base.metadata,
    Column("user_id", ForeignKey("users.chat_id", ondelete="CASCADE"), primary_key=True),
    Column("vacancy_id", ForeignKey("vacancies.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, server_default=func.now())
)