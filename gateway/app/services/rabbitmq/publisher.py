import json
import aio_pika
from app.configs.config import get_channel, declare_fanout_exchange

async def publish_message(message: dict):
    channel = await get_channel()
    exchange = await declare_fanout_exchange(channel)
    result_message = aio_pika.Message(body=json.dumps(message).encode())
    await exchange.publish(result_message, routing_key="")
