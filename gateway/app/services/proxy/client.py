from fastapi import HTTPException
import requests

PROXY_URL = "http://127.0.0.1:8005/upload/"

async def send_image(file, x_api_key, image_bytes):
    try:
 
        files = {"file": (file.filename, image_bytes, file.content_type)}
        response = requests.post(PROXY_URL, files=files, headers={"x-api-key": x_api_key}) 
        return response.json()
    except Exception as e:
        print(f"Error sending image to proxy: {e}")
        #return {"error": str(e)}
        raise HTTPException(status_code=500, detail=str(e))
    
