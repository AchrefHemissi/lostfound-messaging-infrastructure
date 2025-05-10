import aio_pika
import aiohttp
import asyncio
from app.config.config import RABBITMQ_URL
from app.config.config import SERVICE_A_URL, QUEUE_NAME, RESULT_EXCHANGE_NAME, TASK_EXCHANGE_NAME


# Module-level variables
task_queue = None
result_exchange = None


async def get_rabbit_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)

async def setup_rabbitmq_infrastructure():
    """Setup RabbitMQ infrastructure (exchanges and queue)"""

    global task_queue, result_exchange
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()
        
        # Declare exchanges
        task_exchange = await channel.declare_exchange(
            TASK_EXCHANGE_NAME,
            aio_pika.ExchangeType.FANOUT,
            durable=True
        )
        
        result_exchange = await channel.declare_exchange(
            RESULT_EXCHANGE_NAME,
            aio_pika.ExchangeType.FANOUT,
            durable=True
        )
        
        # Declare queue
        task_queue = await channel.declare_queue(
            QUEUE_NAME,
            durable=True,
            auto_delete=False
        )
        
        # Bind queue to exchange
        await task_queue.bind(task_exchange)
        
        return task_exchange, result_exchange, task_queue 