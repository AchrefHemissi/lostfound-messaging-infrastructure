import aio_pika
import aiohttp
import asyncio
from app.config.config import RABBITMQ_URL

async def get_rabbit_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)


