from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import get_db
from api.models.questions import Question
from api.repositories.questions import QuestionRepository
from api.repositories.vacancies import VacancyRepository
from api.schemas.questions import QuestionResponse, QuestionCreationForm, QuestionTypeEnum, QuestionUpdateForm

questions_router = APIRouter(tags=["Questions"], prefix="/questions")

@questions_router.get("/get_all", summary="Get all questions", response_model=list[QuestionResponse])
async def get_questions_router(session: AsyncSession = Depends(get_db)):
    return await QuestionRepository.get_all(session=session)

@questions_router.post("/create", summary="Create new question")
async def create_question_router(form: QuestionCreationForm, session: AsyncSession = Depends(get_db)):
    checkVacancyExists = await VacancyRepository.getVacancy(data=form.vacancy_id, session=session)
    if not checkVacancyExists:
        raise HTTPException(status_code=400, detail="Vacancy with this ID not found!")
    
    checkQuestionTitle = await QuestionRepository.get_question(data=form.title, session=session)
    if checkQuestionTitle:
        raise HTTPException(status_code=400, detail="Question with this title, already exists")
    
    if form.question_type not in [QuestionTypeEnum.TEXT, QuestionTypeEnum.FILE]:
        raise HTTPException(status_code=400, detail="Question type is incorrect. Available only 'tekst' and 'fayl' ")
    
    await QuestionRepository.create_question(form=form.model_dump(), session=session)
    raise HTTPException(status_code=200, detail="Sucessfully created")

@questions_router.put("/update", summary="Update question")
async def update_question_router(form: QuestionUpdateForm, session: AsyncSession = Depends(get_db)):
    checkQuestionExists = await QuestionRepository.get_question(data=form.id, session=session)
    if not checkQuestionExists:
        raise HTTPException(status_code=400, detail="Question with this ID not found")

    checkVacancyExists = await VacancyRepository.getVacancy(data=form.vacancy_id, session=session)
    if not checkVacancyExists:
        raise HTTPException(status_code=400, detail="Vacancy with this ID not found!")
    
    checkQuestionTitle = await QuestionRepository.check_question_for_update(id=form.id, title=form.title, session=session)
    if checkQuestionTitle:
        raise HTTPException(status_code=400, detail="Question with this title, already exists")
    
    if form.question_type not in [QuestionTypeEnum.TEXT, QuestionTypeEnum.FILE]:
        raise HTTPException(status_code=400, detail="Question type is incorrect. Available only 'tekst' and 'fayl' ")
    
    await QuestionRepository.update_question(id=form.id, form=form.model_dump(exclude={"id"}), session=session)
    raise HTTPException(status_code=200, detail="Sucessfully updated")

@questions_router.delete("/delete", summary="Delete question")
async def delete_question_router(id: int, session: AsyncSession = Depends(get_db)):
    checkQuestionExists = await QuestionRepository.get_question(data=id, session=session)
    if not checkQuestionExists:
        raise HTTPException(status_code=400, detail="Question with this ID not found")
    
    await QuestionRepository.delete_question(id=id, session=session)
    raise HTTPException(status_code=200, detail="Sucessfully deleted")