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