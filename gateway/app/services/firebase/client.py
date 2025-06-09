import requests

BASE_FIREBASE_URL = "https://foundit-6ubiti756-leith-engazzous-projects.vercel.app/api/similarity "

async def send_to_firebase(data: dict, route: str = "/receive"):
    firebase_url = f"{BASE_FIREBASE_URL}{route}"
    response = requests.post(firebase_url, json=data)
    return response.status_code