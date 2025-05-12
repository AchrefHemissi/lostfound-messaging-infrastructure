from fastapi import FastAPI, HTTPException
from app.configs.rabbitMQ_config import get_rabbit_connection, setup_rabbitmq_infrastructure
from app.services.consume import consume_task
import asyncio
import logging
import aio_pika

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
consumer_task = None
connection = None

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    global consumer_task, connection
    
    try:
        # First establish connection
        connection = await get_rabbit_connection()
        logger.info("RabbitMQ connection established")
        
        # Then setup infrastructure
        task_queue, result_exchange = await setup_rabbitmq_infrastructure()
        logger.info("RabbitMQ infrastructure setup completed")
        
        # Finally start consumer
        consumer_task = asyncio.create_task(consume_task(task_queue, result_exchange))
        logger.info("Consumer task started successfully")
        
    except aio_pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable - RabbitMQ connection failed")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        if connection:
            await connection.close()
        raise HTTPException(status_code=500, detail="Internal server error during startup")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    global consumer_task, connection
    
    try:
        if consumer_task:
            consumer_task.cancel()
            try:
                await asyncio.wait_for(consumer_task, timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("Consumer task shutdown timed out")
            except asyncio.CancelledError:
                logger.info("Consumer task cancelled successfully")
            except Exception as e:
                logger.error(f"Error during consumer task shutdown: {e}")
        
        if connection:
            try:
                await connection.close()
                logger.info("RabbitMQ connection closed successfully")
            except Exception as e:
                logger.error(f"Error closing RabbitMQ connection: {e}")
                
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
    finally:
        logger.info("Shutdown complete")

@app.get("/")
def read_root():
    return {"message": "Welcome to the LostFound AI Service listener number 1"}

