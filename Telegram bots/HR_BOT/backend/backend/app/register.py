from sqladmin import ModelView
from api.models import users, vacancies, questions, answers

class UserAdmin(ModelView, model=users.User):
    column_list = [users.User.id, users.User.full_name]

    column_labels = {
        "id": "Unikal raqami",
        "chat_id": "Telegram chat ID",
        "full_name": "To'liq ism",
        "username": "Unikal ism",
        "phone_number": "Telefon raqam",
        "vacancy":"Topshirgan vakansiyalari",
        "joined_at": "Qo'shilgan sanasi"
    }

class AnswerAdmin(ModelView, model=answers.Answer):
    column_list = [answers.Answer.id, answers.Answer.text_answer, answers.Answer.question_id]

    column_labels = {
        "id": "Ma'lumot unikal raqami",
        "question_id": "Savolning unikal raqami",
        "text_answer": "Tekst javob",
        "file_answer": "Fayl javob (manzili)"
    }

class VacancyAdmin(ModelView, model=vacancies.Vacancy):
    column_list = [vacancies.Vacancy.id, vacancies.Vacancy.title]

    def count_users(self, obj):
        return len(obj.users)
    
    column_labels = {
        "questions": "Biriktirilgan savollar",
        "user_count": "Ishga topshirganlar soni",
        "question":"Biriktirilgan savollar",
        "users": "Ishga topshirganlar",
        "id":"Ma'lumot unikal raqami",
        "title": "Sarlavha",
        "description":"Batafsil ma'lumot",
        "is_open":"Vakansiya ochiqmi",
        "created_at":"Ma'lumot yaratilgan sana"
    }

class QuestionAdmin(ModelView, model=questions.Question):
    column_list = [questions.Question.id, questions.Question.title]
    form_columns = [questions.Question.title, questions.Question.question_type, questions.Question.is_required]

    column_labels = {
        "id": "Unikal raqami",
        "vacancy_id": "Vakansiya unikal raqami",
        "title": "Sarlavha",
        "question_type": "Savol turi (TEKST yoki FAYL)",
        "is_required": "Majburiymi"
    }