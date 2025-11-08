from sqlalchemy import select, insert, delete
from sqlalchemy.orm import joinedload, with_loader_criteria
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.users import User
from api.models.vacancies import Vacancy
from api.models.questions import Question
from api.models.answers import Answer

class UserRepository:
    async def createUser(session: AsyncSession, form: dict):
        query = insert(User).values(form).returning(User.id)
        execution = await session.execute(query)
        created_id = execution.scalar_one()
        await session.commit()
        return created_id
    
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
            with_loader_criteria(Question, Question.vacancy_id==Vacancy.id)
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