import aio_pika
from app.configs.config import (
    RABBITMQ_URL,
    SERVICE_A_URL,
    QUEUE_NAME,
    RESULT_EXCHANGE_NAME,
    TASK_EXCHANGE_NAME
)

async def get_rabbit_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)

async def get_channel():
    connection = await get_rabbit_connection()
    return await connection.channel()

async def setup_rabbitmq_infrastructure():
    """Setup RabbitMQ infrastructure and return queue + exchanges"""
    channel = await get_channel()
    
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
    
    # Declare and bind queue
    task_queue = await channel.declare_queue(
        QUEUE_NAME,
        durable=True,
        auto_delete=False
    )
    
    await task_queue.bind(task_exchange)
    
    return task_queue, result_exchange
