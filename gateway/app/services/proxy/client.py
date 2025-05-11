import requests

PROXY_URL = "http://localhost:8002/upload/"

def send_image(file):
    try:
        files = {"file": (file.filename, file.file, file.content_type)}
        response = requests.post(PROXY_URL, files=files)
        return response.json()
    except Exception as e:
        print(f"Error sending image to proxy: {e}")
        return {"error": str(e)}
