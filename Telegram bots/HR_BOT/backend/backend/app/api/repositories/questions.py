from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.questions import Question

class QuestionRepository:
    async def get_all(session: AsyncSession):
        query = select(Question)
        execution = await session.execute(query)
        result = execution.scalars().all()
        return result

    async def get_question(data: str | int, session: AsyncSession):
        query = select(Question)

        if isinstance(data, str):
            query = query.where(Question.title==data)
        elif isinstance(data, int):
            query = query.where(Question.id==data)
        execution = await session.execute(query)
        result = execution.scalar_one_or_none()
        return result
    
    async def check_question_for_update(id: int, title: str, session: AsyncSession):
        query = select(Question).where(Question.id!=id, Question.title==title)
        execution = await session.execute(query)
        result = execution.scalar_one_or_none()
        return result
    
    async def create_question(form: dict, session: AsyncSession):
        query = insert(Question).values(form)
        execution = await session.execute(query)
        await session.commit()

    async def update_question(id: int, form: dict, session: AsyncSession):
        query = update(Question).where(Question.id==id).values(form)
        execution = await session.execute(query)
        await session.commit()

    async def delete_question(id: int, session: AsyncSession):
        query = delete(Question).where(Question.id==id)
        execution = await session.execute(query)
        await session.commit()