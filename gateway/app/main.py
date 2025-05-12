from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.services.rabbitmq.publisher import publish_message
from app.services.proxy.client import send_image
from app.services.rabbitmq.consumer import consume_result
import base64
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Globals to keep references for cancellation
suspicious_task = None
similarity_task = None

@app.on_event("startup")
async def startup_event():
    global suspicious_task, similarity_task

    logger.info("Starting consumers...")

    try:
        
        suspicious_task = asyncio.create_task(
            consume_result(
                queue_name="result_suspicious_queue",
                exchange_name="results.suspicious",
                firebase_route="/result/suspicious"
            )
        )

        similarity_task = asyncio.create_task(
            consume_result(
                queue_name="result_similarity_queue",
                exchange_name="results.similarity",
                firebase_route="/result/similarity"
            )
        )

        logger.info("Consumers started successfully")

    except Exception as e:
        logger.error(f"Error starting consumers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during startup")

@app.on_event("shutdown")
async def shutdown_event():
    global suspicious_task, similarity_task

    logger.info("Shutting down consumers...")

    for task_name, task in [("suspicious_task", suspicious_task), ("similarity_task", similarity_task)]:
        if task:
            task.cancel()
            try:
                await asyncio.wait_for(task, timeout=5.0)
                logger.info(f"{task_name} cancelled cleanly")
            except asyncio.TimeoutError:
                logger.warning(f"{task_name} shutdown timed out")
            except asyncio.CancelledError:
                logger.info(f"{task_name} cancelled successfully")
            except Exception as e:
                logger.error(f"Error cancelling {task_name}: {e}")

    logger.info("Shutdown complete")

@app.post("/upload/")
async def upload(
    user_id: str = Form(...),
    post_id: str = Form(...),
    post_type: str = Form(...),
    description: str = Form(...),
    item_category: str = Form(...),
    file: UploadFile = File(...)
):
    try:

        # Read image bytes
        image_bytes = await file.read()

        # Send image to proxy
        proxy_response = send_image(file)
        image_url = proxy_response.get("image_url", "")

        # Encode to base64 for safe JSON transmission
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')

        # Prepare message
        message = {
            "user_id": user_id,
            "post_id": post_id,
            "post_type": post_type,
            "description": description,
            "item_category": item_category,
            "image_data": image_b64,
            "filename": file.filename,       # keep file metadata
            "content_type": file.content_type
        }

        # Publish to RabbitMQ
        await publish_message(message)

        return {"status": "Message received and forwarded.", "image_url": image_url}

    except Exception as e:
        logger.error(f"Error handling upload: {e}")
        raise HTTPException(status_code=500, detail="Failed to process upload")
