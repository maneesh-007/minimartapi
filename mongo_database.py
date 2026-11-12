import os
import dotenv
from beanie import init_beanie
from pymongo import AsyncMongoClient
from models.nosql.activitylog import ActivityLog


dotenv.load_dotenv()


MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME  = os.getenv("MONGO_DB_NAME")

client = None

async def init_mongo():

    global client

    client = AsyncMongoClient(MONGO_URL)

    await init_beanie(
        client[MONGO_DB_NAME],
        document_models=[ActivityLog]
    )

async def close_mongo():
    if client is not None:
        await client.close()
