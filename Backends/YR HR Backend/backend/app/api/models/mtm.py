from sqlalchemy import Table, Column, ForeignKey

from db.connection import Base

user_vacancy_mtm = Table(
    "user_vacancy",
    Base.metadata,
    Column("user_id", ForeignKey("users.chat_id"), primary_key=True),
    Column("vacancy_id", ForeignKey("vacancies.id"), primary_key=True)
)