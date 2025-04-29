```markdown
# Azure Blob Storage Proxy API

This project is a secure FastAPI microservice acting as a proxy layer for uploading and downloading images to/from Azure Blob Storage. It enables controlled access via API keys and is suitable for integration with frontend clients (like Flutter apps) or other microservices (like AI model pipelines or Firebase functions).

## 🚀 Features

- 📤 Upload image files securely to Azure Blob Storage
- 📥 Download image files by name
- 🔐 API key validation for upload and download routes
- ☁️ Environment variable support (.env) for configuration

## 📁 Project Structure

```
proxy-layer/
│
├── app/
│   ├── main.py            # Main FastAPI app
│   └── dependencies.py    # API key validation logic
│
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 🔧 Requirements

- Python 3.10+
- Azure Storage Account with a Blob Container

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🌍 Environment Variables (.env)

Create a `.env` file in the root directory:

```env
AZURE_STORAGE_CONNECTION_STRING=your_azure_connection_string
AZURE_CONTAINER_NAME=your_container_name
AUTHORIZED_UPLOAD_KEYS=your_upload_key1,your_upload_key2
AUTHORIZED_AI_KEYS=your_ai_key1,your_ai_key2
```

## 🧪 API Usage

### Upload Image

- Endpoint: `POST /upload/`
- Headers:
  - `x-api-key`: your authorized upload key
- Body (multipart/form-data):
  - `file`: image file (e.g., .jpg, .png)

✅ Example using curl:

```bash
curl -X POST http://localhost:8000/upload/ \
  -H "x-api-key: your_upload_key" \
  -F "file=@image.jpg"
```

### Download Image

- Endpoint: `GET /download/{blob_name}`
- Headers:
  - `x-api-key`: your authorized AI key

✅ Example:

```bash
curl -X GET http://localhost:8000/download/image.jpg \
  -H "x-api-key: your_ai_key" --output image.jpg
```

### Delete Image

- Endpoint: `DELETE /delete/{blob_name}`
- Headers:
  - `x-api-key`: your authorized upload key

✅ Example:

```bash
curl -X DELETE http://localhost:8000/delete/image.jpg \
  -H "x-api-key: your_upload_key"
```

## 🧰 Notes

- Upload keys and AI keys are validated independently
- Images are returned with correct MIME types (image/jpeg, image/png, etc.)
- Error handling is built-in for missing keys or blobs

## 📦 Deployment

To run locally:

```bash
uvicorn app.main:app --reload
```

Or in production:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📄 License

MIT License
```
