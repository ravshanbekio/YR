from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.vacancies import Vacancy

class VacancyRepository:
    async def getAll(session: AsyncSession):
        query = select(Vacancy)
        execution = await session.execute(query)
        result = execution.scalars().all()
        return result
    
    async def getVacancy(session: AsyncSession, data: str | int):
        query = select(Vacancy)
        if isinstance(data, str):
            query = query.where(Vacancy.title==data)
        elif isinstance(data, int):
            query = query.where(Vacancy.id==data)
            
        query = query.options(joinedload(Vacancy.questions))
        execution = await session.execute(query)
        result = execution.unique().scalar_one_or_none()
        return result
    
    async def createVacancy(form: dict, session: AsyncSession):
        query = insert(Vacancy).values(form)
        execution = await session.execute(query)
        await session.commit()
        
    async def updateVacancy(id: int, form: dict, session: AsyncSession):
        query = update(Vacancy).where(Vacancy.id==id).values(form)
        execution = await session.execute(query)
        await session.commit()

    async def deleteVacancy(id: int, session: AsyncSession):
        query = delete(Vacancy).where(Vacancy.id==id)
        execution = await session.execute(query)
        await session.commit()