import httpx
from credentials import BASE_URL

async def get_user(chat_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/get_user", params={"chat_id":chat_id})
        if response.status_code == 200:
            return response.json()
        return None
    
async def create_user(chat_id: int, full_name: str, username: str = None, phone_number: str = None):
    async with httpx.AsyncClient() as client:
        data = {
            "chat_id":str(chat_id),
            "full_name": full_name,
            "username":username,
            "phone_number":phone_number
        }
        response = await client.post(f"{BASE_URL}/users/create", json=data)
        if response.status_code == 200:
            return response.json()
        return response.text