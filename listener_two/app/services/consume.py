import aio_pika
import aiohttp
import json
import base64
from app.configs.rabbitMQ_config import get_rabbit_connection
from app.configs.config import SERVICE_A_URL
from app.models.message_receive import Message_receive
from app.models.message_send import Message_send


async def consume_task(task_queue, result_exchange):


    async with task_queue.iterator() as task_queue_iter:
        async for message in task_queue_iter:
            print("Consuming task")
            async with message.process():
                try:
                    received_data = json.loads(message.body.decode())
                    cleaned_data = {
                        k: v.strip() if isinstance(v, str) else v
                        for k, v in received_data.items()
                    }
                    received_message = Message_receive(**cleaned_data)
                except Exception as e:
                    print(f"Invalid message format: {e}")
                    await message.nack(requeue=False)
                    continue

                try:
                    image_bytes = base64.b64decode(received_message.image_data)
                except Exception as e:
                    print(f"Failed to decode image data: {e}")
                    await message.nack(requeue=False)
                    continue

                data = aiohttp.FormData()
                data.add_field("user_id", received_message.user_id)
                data.add_field("image_file", image_bytes, filename=received_message.filename, content_type=received_message.content_type)
                data.add_field("post_id", received_message.post_id)
                data.add_field("post_type", received_message.post_type)
                data.add_field("text", received_message.description)
                data.add_field("item_type", received_message.item_category)

                print(f"Service A: Processing task")

                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(SERVICE_A_URL, data=data) as response:
                            if response.status == 200:
                                result = await response.json()
                                result_message = aio_pika.Message(body=json.dumps(result).encode())
                                await result_exchange.publish(result_message, routing_key="")
                                print(f"Service A: Task processed successfully")
                            else:
                                print("Service A failed, requeuing.")
                                await message.nack(requeue=False) #bad handling must be improved
                except Exception as e:
                    print(f"Error occurred: {e}")
                    await message.nack(requeue=False)
