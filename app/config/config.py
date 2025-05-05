import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv


print("Loading environment variables...")

load_dotenv()

print("Environment variables loaded.")

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