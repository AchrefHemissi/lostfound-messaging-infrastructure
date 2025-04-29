from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Request
from fastapi.responses import StreamingResponse
from azure.storage.blob import BlobServiceClient, ContentSettings, generate_blob_sas, BlobSasPermissions
from dotenv import load_dotenv
from datetime import datetime, timedelta
import mimetypes
import os
import io

load_dotenv()

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

if not AZURE_CONNECTION_STRING:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set. Check your .env file.")
if not CONTAINER_NAME:
    raise ValueError("AZURE_CONTAINER_NAME is not set. Check your .env file.")


UPLOAD_KEYS = set(os.getenv("AUTHORIZED_UPLOAD_KEYS", "").split(","))
AI_KEYS = set(os.getenv("AUTHORIZED_AI_KEYS", "").split(","))

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

app = FastAPI()

def validate_api_key(api_key: str | None, allowed_keys: set):
    if not api_key or api_key not in allowed_keys:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Azure Blob Storage API"}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), x_api_key: str = Header(None)):
    validate_api_key(x_api_key, UPLOAD_KEYS)

    blob_name = f"{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}_{file.filename}"
    blob_client = container_client.get_blob_client(blob_name)

    try:
        blob_client.upload_blob(
            await file.read(),
            overwrite=True,
            content_settings=ContentSettings(content_type=file.content_type)
        )
        return {"status": "success", "blob_name": blob_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{blob_name}")
def download_image(blob_name: str, x_api_key: str = Header(None)):
    validate_api_key(x_api_key, AI_KEYS)

    blob_client = container_client.get_blob_client(blob_name)

    try:
        blob_data = blob_client.download_blob()
        stream = io.BytesIO(blob_data.readall())

        # Detect the MIME type (e.g., image/jpeg, image/png)
        mime_type, _ = mimetypes.guess_type(blob_name)
        content_type = mime_type or "application/octet-stream"

        return StreamingResponse(stream, media_type=content_type)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Blob not found or error occurred")
    

@app.delete("/remove/{blob_name}")
def remove_image(blob_name: str, x_api_key: str = Header(None)):
    validate_api_key(x_api_key, UPLOAD_KEYS)  

    blob_client = container_client.get_blob_client(blob_name)

    try:
        blob_client.delete_blob()
        return {"status": "success", "message": f"{blob_name} has been deleted."}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to delete blob: {str(e)}")