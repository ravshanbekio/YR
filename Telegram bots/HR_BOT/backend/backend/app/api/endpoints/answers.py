from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import get_db
from api.repositories.answers import AnswerRepository
from api.repositories.questions import QuestionRepository
from api.repositories.users import UserRepository
from api.repositories.mtm import MTMRepository
from api.repositories.vacancies import VacancyRepository
from api.schemas.answers import AnswerCreationForm

answers_router = APIRouter(tags=["Answers"], prefix="/answers")

@answers_router.post("/create_answer", summary="Create an answer for question")
async def create_answer_router(form: AnswerCreationForm, session: AsyncSession = Depends(get_db)):
    checkUserExists = await UserRepository.checkUserByChatID(chat_id=form.user_id, session=session)
    if not checkUserExists:
        raise HTTPException(status_code=400, detail="User doesn't exist")
    
    checkVacancyExists = await VacancyRepository.getVacancy(data=form.vacancy_id, session=session)
    if not checkVacancyExists:
        raise HTTPException(status_code=400, detail="Vacancy with this ID, not found")

    checkQuestionExists = await QuestionRepository.get_question(data=form.question_id, session=session)
    if not checkQuestionExists:
        raise HTTPException(status_code=400, detail="Question doesn't exist")

    
    if form.text_answer is None and form.file_answer is None:
        raise HTTPException(status_code=400, detail="Both answers type is empty (null)")
    
    checkMTMExists = await MTMRepository.get_mtm(user_id=form.user_id, vacancy_id=form.vacancy_id, session=session)
    if not checkMTMExists:
        await MTMRepository.create_mtm(user_id=form.user_id, vacancy_id=form.vacancy_id, session=session)
        
    await AnswerRepository.create_answer(form=form.model_dump(exclude={"vacancy_id"}), session=session)
    raise HTTPException(status_code=200, detail="Sucessfully created")