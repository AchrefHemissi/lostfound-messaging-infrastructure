from fastapi import FastAPI
from app.config.rabbitMQ_config import  get_rabbit_connection
from app.service.consume import consume_task
import asyncio

app = FastAPI()
consumer_task = None
connection = None

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    global consumer_task, connection
    connection = await get_rabbit_connection()
    consumer_task = asyncio.create_task(consume_task())
    print("Started")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    global consumer_task, connection
    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
    if connection:
        await connection.close()
    print("Shutdown complete")

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the LostFound AI Service listener number 1"}

