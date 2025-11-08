from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqladmin import Admin
from redis.exceptions import ConnectionError

from db.connection import engine
from register import UserAdmin, VacancyAdmin, QuestionAdmin, AnswerAdmin
from api.endpoints import users, vacancies, answers, questions
from utils.caching import redis_client

app = FastAPI(default_response_class=ORJSONResponse)

@app.on_event("startup")
async def startup_event():
    try:
        await redis_client.ping()
        await redis_client.flushall()
    except ConnectionError:
        print("Couldn't connect redis")

@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.flushall() # Clear all data from redis
    await redis_client.close()

# Routers
app.include_router(users.users_router)
app.include_router(vacancies.vacancies_router)
app.include_router(answers.answers_router)
app.include_router(questions.questions_router)

# Registers for Admin Panel
admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(VacancyAdmin)
admin.add_view(AnswerAdmin)
admin.add_view(QuestionAdmin)