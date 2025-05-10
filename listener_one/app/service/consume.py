import aio_pika
import aiohttp
from app.config.rabbitMQ_config import get_rabbit_connection
from app.config.config import SERVICE_A_URL, QUEUE_NAME, RESULT_EXCHANGE_NAME, TASK_EXCHANGE_NAME



async def consume_task():
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()

        # Declare the queue
        task_queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        result_exchange = await channel.declare_exchange(RESULT_EXCHANGE_NAME, aio_pika.ExchangeType.FANOUT)

        # Bind the queue to the exchange
        await task_queue.bind(TASK_EXCHANGE_NAME) 

        # Consume messages from the queue
        async for message in task_queue:
            async with message.process():
                task = message.body.decode()
                print(f"Service A: Processing task: {task}")
                
                # Send HTTP request to Service A
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(SERVICE_A_URL, json={"content": task}) as response:
                            if response.status == 200:
                                result = await response.json()
                                result_message = aio_pika.Message(body=str(result).encode())
                                await result_exchange.publish(result_message, routing_key='')
                            else:
                                # If the service is unavailable or returns an error, requeue the message
                                print("Service A failed to respond, requeuing message.")
                                await task_queue.publish(message)
                except Exception as e:
                    print(f"Error occurred: {e}")
                    # Requeue the message if an error occurs
                    await task_queue.publish(message)