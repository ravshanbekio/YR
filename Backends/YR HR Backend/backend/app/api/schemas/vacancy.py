from pydantic import BaseModel

from api.schemas.questions import QuestionAnswerResponse

class VacancyResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_open: bool

    class Config:
        from_attributes = True

class VacancyDetailResponse(VacancyResponse):
    questions: list[QuestionAnswerResponse] = []

    class Config:
        from_attributes = True

class VacancyCreationForm(BaseModel):
    title: str
    description: str | None = None
    is_open: bool = True

class VacancyUpdateForm(BaseModel):
    id: int
    title: str | None
    description: str | None = None
    is_open: bool | str