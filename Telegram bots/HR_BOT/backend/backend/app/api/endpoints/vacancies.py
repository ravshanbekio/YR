import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis.exceptions import ConnectionError
from datetime import datetime

from db.connection import get_db
from api.repositories.vacancies import VacancyRepository
from api.schemas.vacancy import VacancyResponse, VacancyDetailResponse, VacancyCreationForm, VacancyUpdateForm
from utils.caching import redis_client

vacancies_router = APIRouter(tags=["Vacancies"], prefix="/vacancies")

@vacancies_router.get("/get_all", 
                      summary="Get all vacancies list", 
                      response_model=list[VacancyResponse]                      
                    )
async def get_vacancies_router(
    session: AsyncSession = Depends(get_db)
    ):
    try:
        cached_data = await redis_client.get("all_vacancies")
        if not cached_data:
            objects = await VacancyRepository.getAll(session=session)
            data = [VacancyResponse.from_orm(object).dict() for object in objects]
            await redis_client.set("all_vacancies", json.dumps(data), ex=604800) # Caching for 7 days
            return objects

        return json.loads(cached_data)
    except ConnectionError:
        print("Couldn't connect redis")
        return [
            {
                "id":0,
                "title":"string",
                "description":"string",
                "is_open": False
            }
        ]

@vacancies_router.get("/get_vacancy", summary="Get vacancy by ID", response_model=VacancyDetailResponse)
async def get_vacancy_router(id: int = None,
                             title: str = None, 
                             session: AsyncSession = Depends(get_db)
                            ):
    try:
        if id is None and title is None:
            raise HTTPException(status_code=400, detail="ID or Title is missing!")
        
        data = id if title is None else title
        cached = await redis_client.get(f"vacancy_{data}")
        if not cached:
            checkVacancyExists = await VacancyRepository.getVacancy(session=session, data=data)
            if not checkVacancyExists:
                raise HTTPException(status_code=400, detail="Vacancy does not exist")
            
            vacancy_dict = VacancyDetailResponse.from_orm(checkVacancyExists).dict()
            await redis_client.set(f"vacancy_{data}", json.dumps(vacancy_dict), ex=2628000) # Caching for 1 month
            return checkVacancyExists
        print("Coming from cached")
        return json.loads(cached)
    except ConnectionError:
        print("Couldn't connect redis")
        return {
            {
                "id":0,
                "title":"string",
                "description":"string",
                "is_open": False,
                "questions": []
            }
        }
    
@vacancies_router.post("/create", summary="Create new vacancy")
async def vacancy_creation_router(form: VacancyCreationForm, session: AsyncSession = Depends(get_db)):
    checkTitle = await VacancyRepository.getVacancy(data=form.title, session=session)
    if checkTitle:
        raise HTTPException(status_code=400, detail="Vacancy already exists")
    
    form = form.model_dump()
    form['created_at'] = datetime.now()
    vacancy_id = await VacancyRepository.createVacancy(form=form, session=session)

    # Caching for all objects update
    try:
        cached_data = await redis_client.get("all_vacancies")
        if cached_data:
            convert_to_dict = json.loads(cached_data)
            await redis_client.delete("all_vacancies")
            convert_to_dict.append({
                "id": vacancy_id,
                "title": form["title"],
                "description": form["description"],
                "is_open": form["is_open"]
            })
            await redis_client.set("all_vacancies", json.dumps(convert_to_dict), ex=604800) # Caching for 7 days
    except ConnectionError:
        print("Couldn't connect redis")
    raise HTTPException(status_code=200, detail="Succesfully created")

@vacancies_router.put("/update", summary="Update vacancy")
async def vacancy_update_router(form: VacancyUpdateForm, session: AsyncSession = Depends(get_db)):
    checkVacancyExists = await VacancyRepository.getVacancy(data=form.id, session=session)
    if not checkVacancyExists:
        raise HTTPException(status_code=400, detail="Vacancy with this ID not found!")
    
    checkTitle = await VacancyRepository.getVacancy(data=form.title, session=session)
    if checkTitle:
        raise HTTPException(status_code=400, detail="Vacancy already exists")
    
    await VacancyRepository.updateVacancy(id=form.id, form=form.model_dump(exclude={"id"}), session=session)

    # Caching for all objects update
    try:
        cached_vacancies = await redis_client.get("all_vacancies")
        if cached_vacancies:
            convert_to_dict = json.loads(cached_vacancies)
            await redis_client.delete("all_vacancies")
            for vacancy in convert_to_dict:
                if vacancy["id"] == form.id:
                    vacancy["title"] = form.title
                    vacancy["description"] = form.description
                    vacancy["is_open"] = form.is_open

            await redis_client.set("all_vacancies", json.dumps(convert_to_dict), ex=604800) # Caching for 7 days
            
        # Update individual vacancy cache
        cached_vacancy = await redis_client.get(f"vacancy_{form.id}")
        if cached_vacancy:
            await redis_client.delete(f"vacancy_{form.id}")
            vacancy_dict = {
                "id": form.id,
                "title": form.title,
                "description": form.description,
                "is_open": form.is_open,
                "questions": checkVacancyExists.questions
            }
            await redis_client.set(f"vacancy_{form.id}". json.dumps(vacancy_dict), ex=2628000) # Caching for 1 month
            raise HTTPException(status_code=200, detail="Successfully updated")
    except ConnectionError:
        print("Couldn't connect redis")

@vacancies_router.delete("/delete", summary="Delete vacancy")
async def vacancy_delete_router(id: int, session: AsyncSession = Depends(get_db)):
    checkVacancyExists = await VacancyRepository.getVacancy(data=id, session=session)
    if not checkVacancyExists:
        raise HTTPException(status_code=400, detail="Vacancy with this ID not found!") 
    
    try:
        cached_vacancies = await redis_client.get("all_vacancies")
        if cached_vacancies:
            convert_to_dict = json.loads(cached_vacancies)
            updated_vacancies_list = []
            for vacancy in convert_to_dict:
                if vacancy["id"] != id:
                    updated_vacancies_list.append(vacancy)
                    
            await redis_client.delete("all_vacancies")
            await redis_client.set("all_vacancies", json.dumps(updated_vacancies_list), ex=604800) # Caching for 7 days

        await redis_client.delete(f"vacancy_{id}")
        await VacancyRepository.deleteVacancy(id=id, session=session)
        raise HTTPException(status_code=200, detail="Successfully deleted")
    except ConnectionError:
        print("Couldn't connect redis")