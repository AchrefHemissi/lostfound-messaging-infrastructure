import io
import mimetypes
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from fastapi.responses import StreamingResponse
from azure.storage.blob import ContentSettings
from app.config.config import UPLOAD_KEYS, AI_KEYS, container_client
from app.dependencies import validate_api_key
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],  # Allows all origins - adjust this in production!
     allow_credentials=True,
     allow_methods=["*"], 
     allow_headers=["*"], 
 )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Azure Blob Storage API"}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), x_api_key: str = Header(None)):
    validate_api_key(x_api_key, UPLOAD_KEYS)

    # Check if the file is a photo 
    allowed_mime_types = {"image/jpeg", "image/png", "image/gif"}
    if file.content_type not in allowed_mime_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type"
        )

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
        raise HTTPException(status_code=404, detail="Error occurred while uploading")


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
        raise HTTPException(status_code=404, detail="Error occurred") 
    

@app.delete("/remove/{blob_name}")
def remove_image(blob_name: str, x_api_key: str = Header(None)):
    validate_api_key(x_api_key, UPLOAD_KEYS)  

    blob_client = container_client.get_blob_client(blob_name)

    try:
        blob_client.delete_blob()
        return {"status": "success", "message": f"{blob_name} has been deleted."}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to delete blob") # i added this to make it more generic and not expose the blob name in the error message