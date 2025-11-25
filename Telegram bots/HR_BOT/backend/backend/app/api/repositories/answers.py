from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.answers import Answer

class AnswerRepository:
    async def create_answer(session: AsyncSession, form: dict):
        query = insert(Answer).values(form)
        execution = await session.execute(query)
        await session.commit()