from fastapi import FastAPI
from routes.appinfo import appinfo_router
from contextlib import asynccontextmanager

from mongo_database import init_mongo,close_mongo
from routes.activitylog import activity_router
from routes.customer import customer_routes

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_mongo()
    yield
    await close_mongo()



app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Welcom e to the Minimart API!"}

app.include_router(appinfo_router)
app.include_router(activity_router)
app.include_router(customer_routes)