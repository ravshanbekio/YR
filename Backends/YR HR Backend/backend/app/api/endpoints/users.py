from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from db.connection import get_db
from api.repositories.users import UserRepository
from api.schemas.users import UserCreationForm, UserResponse

users_router = APIRouter(tags=["Users"], prefix="/users")

@users_router.post("/create", summary="Create new user")
async def create_user_router(form: UserCreationForm, session: AsyncSession = Depends(get_db)):
    checkChatID = await UserRepository.checkUserByChatID(session=session, chat_id=form.chat_id)
    if checkChatID:
        user = checkChatID.id
    else:
        data = {
            "chat_id":form.chat_id,
            "full_name":form.full_name,
            "username":form.username,
            "phone_number": form.phone_number,
            "joined_at": datetime.now()
        }
        user = await UserRepository.createUser(session=session, form=data) 
    raise HTTPException(detail="Successfully created", status_code=200)

@users_router.get("/get_user", summary="Get user by chat ID", response_model=UserResponse)
async def get_user_router(chat_id: str, session: AsyncSession = Depends(get_db)):
    user = await UserRepository.checkUserByChatID(session=session, chat_id=chat_id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")                                                       

    return user