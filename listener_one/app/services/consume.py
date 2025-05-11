import aio_pika
import aiohttp
import json
from app.configs.rabbitMQ_config import get_rabbit_connection
from app.configs.config import SERVICE_A_URL, QUEUE_NAME, RESULT_EXCHANGE_NAME, TASK_EXCHANGE_NAME
from app.models.message_receive import Message_receive
from app.models.message_send import Message_send
from app.configs.rabbitMQ_config import task_queue, result_exchange


async def consume_task():
        
        # Consume messages from the queue
        async for message in task_queue: # This is an infinite loop that keeps running
            print("Consuming task")
            async with message.process():
                # Parse the received message into Message_receive model
                received_data = json.loads(message.body.decode())
                received_message = Message_receive(**received_data)
                
                # Transform to Message_send format
                send_message = Message_send(
                    post_id=received_message.post_id,
                    post_type=received_message.post_type,
                    image_url=received_message.image_data,  
                    text=received_message.description,      
                    item_type=received_message.item_category 
                )
                
                print(f"Service A: Processing task: {send_message.dict()}")
                
                # Send HTTP request to Service A
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(SERVICE_A_URL, json=send_message.dict()) as response:
                            if response.status == 200:
                                result = await response.json()
                                result_message = aio_pika.Message(body=str(result).encode())
                                await result_exchange.publish(result_message)
                            else:
                                print("Service A failed to respond, requeuing message.")
                                await task_queue.publish(message)
                except Exception as e:
                    print(f"Error occurred: {e}")
                    await task_queue.publish(message)