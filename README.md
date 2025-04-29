
# 🧊 Azure Blob Storage Proxy API

```markdown

A lightweight and secure FastAPI microservice that acts as a proxy for uploading and downloading images to and from Azure Blob Storage. Built for seamless integration with frontend clients (like Flutter apps) or other microservices (like AI pipelines or Firebase functions).

```
## ✨ Features

- ✅ Secure image uploads to Azure Blob Storage
- ✅ Secure image downloads with proper content-type headers
- ✅ Image deletion endpoint
- 🔐 API Key authentication
- 📦 .env-based configuration

---

## 🗂️ Project Structure

proxy-layer/
├── app/
│   ├── main.py            # FastAPI routes
│   └── dependencies.py    # API key validation
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## ⚙️ Setup

1. Clone the repo:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```env
AZURE_STORAGE_CONNECTION_STRING=your_azure_blob_connection_string
AZURE_CONTAINER_NAME=your_container_name
AUTHORIZED_UPLOAD_KEYS=your_upload_key1,your_upload_key2
AUTHORIZED_AI_KEYS=your_ai_key1,your_ai_key2
```

---

## 🚀 Run the Server

```bash
uvicorn app.main:app --reload
```

> Runs on http://localhost:8000 by default

---

## 📤 Upload an Image

- URL: `POST /upload/`
- Headers:
  - `x-api-key: your_upload_key`
- Body: `multipart/form-data`
  - Field: `file` → (image file)

```bash
curl -X POST http://localhost:8000/upload/ \
  -H "x-api-key: your_upload_key" \
  -F "file=@path/to/image.jpg"
```

---

## 📥 Download an Image

- URL: `GET /download/{blob_name}`
- Headers:
  - `x-api-key: your_ai_key`

```bash
curl -X GET http://localhost:8000/download/example.jpg \
  -H "x-api-key: your_ai_key" --output downloaded.jpg
```

- Returned with correct MIME type (e.g., image/jpeg)

---

## ❌ Delete an Image

- URL: `DELETE /delete/{blob_name}`
- Headers:
  - `x-api-key: your_upload_key`

```bash
curl -X DELETE http://localhost:8000/delete/example.jpg \
  -H "x-api-key: your_upload_key"
```

---

## 🧪 Test with Postman

1. Import the endpoints.
2. Add the appropriate `x-api-key` header.
3. Use `form-data` for image uploads.
4. For download, use `Send and Download` to receive the image.

---

## 📄 License

This project is licensed under the MIT License.

---
