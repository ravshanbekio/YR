from pydantic import BaseModel
from api.schemas.vacancy import VacancyDetailResponse

class UserCreationForm(BaseModel):
    chat_id: str
    full_name: str
    username: str = None
    phone_number: str


class UserResponse(BaseModel):
    id: int
    chat_id: str
    full_name: str
    username: str | None = None
    phone_number: str

    vacancy: list[VacancyDetailResponse] = []