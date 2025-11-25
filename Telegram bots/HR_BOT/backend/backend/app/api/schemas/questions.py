from pydantic import BaseModel
from typing import Optional
from enum import Enum

from api.schemas.answers import AnswerResponse

class QuestionTypeEnum(str, Enum):
    TEXT = "tekst"
    FILE = "fayl"

class QuestionResponse(BaseModel):
    id: int
    title: str
    question_type: str
    is_required: bool

    class Config:
        from_attributes = True

class QuestionAnswerResponse(BaseModel):
    id: int
    title: str
    question_type: str
    is_required: bool
    answer: AnswerResponse | None = None

    class Config:
        from_attributes = True

class QuestionCreationForm(BaseModel):
    vacancy_id: int
    title: str
    question_type: QuestionTypeEnum
    is_required: bool

class QuestionUpdateForm(BaseModel):
    id: int
    vacancy_id: Optional[int]
    title: Optional[str]
    question_type: Optional[QuestionTypeEnum]
    is_required: Optional[bool]