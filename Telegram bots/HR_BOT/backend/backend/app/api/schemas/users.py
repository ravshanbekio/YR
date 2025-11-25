from pydantic import BaseModel
from api.schemas.vacancy import VacancyAnswerResponse

class UserCreationForm(BaseModel):
    chat_id: str
    full_name: str
    username: str | None= None
    phone_number: str | None = None

class UserResponse(BaseModel):
    id: int
    chat_id: str
    full_name: str
    username: str | None = None
    phone_number: str| None = None

class UserVacancyResponse(BaseModel):
    chat_id: str
    full_name: str
    username: str | None = None
    title: str

class UserDetailResponse(UserResponse):
    vacancy: list[VacancyAnswerResponse] = []