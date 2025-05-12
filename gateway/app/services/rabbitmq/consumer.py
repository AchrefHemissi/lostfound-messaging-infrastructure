import json
import logging
from app.configs.config import get_channel, declare_result_exchange
from app.services.firebase.client import send_to_firebase

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_result(queue_name: str, exchange_name: str, firebase_route: str):
    channel = await get_channel()
    exchange = await declare_result_exchange(channel, exchange_name)
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body.decode())
                logger.info(f"Received message from exchange '{exchange_name}' for queue '{queue_name}'")
                try:
                    await send_to_firebase(data, route=firebase_route)
                    logger.info(f"Forwarded message to Firebase route: {firebase_route}")
                except Exception as e:
                    logger.error(f"Error sending message to Firebase: {e}")
