from sqlalchemy import select, insert, delete
from sqlalchemy.orm import joinedload, with_loader_criteria
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.users import User
from api.models.vacancies import Vacancy
from api.models.questions import Question
from api.models.answers import Answer
from api.models.mtm import user_vacancy_mtm

class UserRepository:
    async def createUser(session: AsyncSession, form: dict):
        query = insert(User).values(form).returning(User.id)
        execution = await session.execute(query)
        created_id = execution.scalar_one()
        await session.commit()
        return created_id

    async def getRecentApplications(session: AsyncSession, limit: int = 10):
        query = select(
            User.chat_id,
            User.full_name,
            User.username,
            Vacancy.title
        ).select_from(user_vacancy_mtm).join(
            User, User.chat_id == user_vacancy_mtm.c.user_id
        ).join(
            Vacancy, Vacancy.id == user_vacancy_mtm.c.vacancy_id
        ).order_by(user_vacancy_mtm.c.created_at.desc())
        execution = await session.execute(query)
        result = execution.all()
        return result

    async def getUserByID(session: AsyncSession, id: int):
        query = select(User).where(User.id==id)
        execution = await session.execute(query)
        result = execution.scalar_one_or_none()
        return result

    async def checkUserByChatID(session: AsyncSession, chat_id: int):
        query = select(User).where(User.chat_id==chat_id).options(
            joinedload(User.vacancy)
            .joinedload(Vacancy.questions)
            .joinedload(Question.answer),
            with_loader_criteria(Answer, Answer.user_id==chat_id)
        )
        """
        .options(
        joinedload(User.vacancy)
            .joinedload(Vacancy.questions)
            .joinedload(Question.answers),
        with_loader_criteria(Answer, Answer.user_id==chat_id)
        )"""
        execution = await session.execute(query)
        result = execution.unique().scalar_one_or_none()
        return result   