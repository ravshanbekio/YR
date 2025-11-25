import httpx
from credentials import BASE_URL

async def get_vacancies():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/vacancies/get_all")
        if response.status_code == 200:
            return response.json()
        return []
    
async def get_vacancy(data: str | int):
    async with httpx.AsyncClient() as client:
        if isinstance(data, str):
            query_param = "title"
        elif isinstance(data, int):
            query_param = "id"
        response = await client.get(f"{BASE_URL}/vacancies/get_vacancy", params={query_param: data})
        if response.status_code == 200:
            return response.json()
        return None
    
async def save_answer(chat_id: int, vacancy_id: int, question_id: int, answer: str):
    async with httpx.AsyncClient() as client:
        data = {
            "user_id":str(chat_id),
            "vacancy_id":vacancy_id,
            "question_id": question_id,
            "text_answer":answer,
            "file_answer": None
        }
        response = await client.post(f"{BASE_URL}/answers/create_answer", json=data)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            return response.text
        return response.text