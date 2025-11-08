from pydantic import BaseModel

class AnswerResponse(BaseModel):
    id: int
    user_id: str
    question_id: int
    text_answer: str = None
    file_answer: str = None

    class Config:
        from_attributes = True

class AnswerCreationForm(BaseModel):
    user_id: str
    vacancy_id: int
    question_id: int
    text_answer: str = None
    file_answer: str = None