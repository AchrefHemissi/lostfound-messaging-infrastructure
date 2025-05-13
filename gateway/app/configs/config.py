import aio_pika # type: ignore
from aio_pika import ExchangeType # type: ignore

RABBITMQ_URL = "amqp://myuser:mypassword@localhost/"

TASK_EXCHANGE_NAME = "gateway_fanout_exchange"

async def get_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)

async def get_channel():
    connection = await get_connection()
    return await connection.channel()

async def declare_fanout_exchange(channel):
    return await channel.declare_exchange(TASK_EXCHANGE_NAME, aio_pika.ExchangeType.FANOUT, durable=True)

async def declare_result_exchange(channel, name):
    return await channel.declare_exchange(name, aio_pika.ExchangeType.FANOUT, durable=True)