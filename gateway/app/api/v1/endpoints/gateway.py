from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel
from typing import Literal, Optional
import aio_pika
import json
from io import BytesIO

app = FastAPI()

class MessageReceive(BaseModel):
    user_id: str
    post_id: str
    post_type: Literal["lostitem", "founditem"]
    description: str
    item_category: str

async def get_rabbitmq_connection():
    # Connect to RabbitMQ
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/"
    )
    return connection

@app.post("/receive-message")
async def receive_message(
    user_id: str = Form(...),
    post_id: str = Form(...),
    post_type: Literal["lostitem", "founditem"] = Form(...),
    description: str = Form(...),
    item_category: str = Form(...),
    image: UploadFile = File(None)
):
    # Connect to RabbitMQ
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    
    # Declare the queues
    metadata_queue = await channel.declare_queue("lost_found_metadata")
    image_queue = await channel.declare_queue("lost_found_images")
    
    try:
        # Create metadata message
        metadata = MessageReceive(
            user_id=user_id,
            post_id=post_id,
            post_type=post_type,
            description=description,
            item_category=item_category
        )

        # Send metadata
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(metadata.dict()).encode(),
                content_type="application/json",
                headers={
                    "post_id": post_id,
                    "message_type": "metadata"
                }
            ),
            routing_key="lost_found_metadata"
        )

        # If image is provided, send it as raw bytes
        if image:
            image_bytes = await image.read()
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=image_bytes,  # Raw binary data
                    content_type=image.content_type,
                    headers={
                        "post_id": post_id,
                        "message_type": "image",
                        "filename": image.filename
                    }
                ),
                routing_key="lost_found_images"
            )
        
        return {
            "status": "success", 
            "message": "Message received and sent to queue",
            "post_id": post_id
        }
    
    finally:
        await connection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)