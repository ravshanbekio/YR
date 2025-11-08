from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.mtm import user_vacancy_mtm

class MTMRepository:
    async def create_mtm(session: AsyncSession, user_id: str, vacancy_id: int):
        query = insert(user_vacancy_mtm).values(user_id=user_id, vacancy_id=vacancy_id)
        execution = await session.execute(query)
        await session.commit()

    async def get_mtm(session: AsyncSession, user_id: int, vacancy_id: int):
        query = select(user_vacancy_mtm).where(user_vacancy_mtm.c.user_id==user_id, user_vacancy_mtm.c.vacancy_id==vacancy_id)
        execution = await session.execute(query)
        result = execution.scalar_one_or_none()
        return result