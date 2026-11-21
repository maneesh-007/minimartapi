import os
import dotenv
from beanie import init_beanie
from pymongo import AsyncMongoClient
from models.nosql.activitylog import ActivityLog
from models.nosql.product import Product
from models.nosql.category import Category


dotenv.load_dotenv()


MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME  = os.getenv("MONGO_DB_NAME")

client = None

async def init_mongo():

    global client

    client = AsyncMongoClient(MONGO_URL)

    await init_beanie(
        client[MONGO_DB_NAME],
        document_models=[ActivityLog,Product,Category]
    )

async def close_mongo():
    if client is not None:
        await client.close()
