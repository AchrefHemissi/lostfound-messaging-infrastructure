import requests

BASE_FIREBASE_URL = "https://your-firebase-endpoint.com"

async def send_to_firebase(data: dict, route: str = "/receive"):
    firebase_url = f"{BASE_FIREBASE_URL}{route}"
    response = requests.post(firebase_url, json=data)
    return response.status_code