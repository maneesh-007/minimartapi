from fastapi import FastAPI,security
from fastapi.middleware.cors import CORSMiddleware
from routes.appinfo import appinfo_router
from contextlib import asynccontextmanager

from mongo_database import init_mongo,close_mongo
from routes.activitylog import activity_router
from routes.customer import customer_routes
from routes.product import product_routes
@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_mongo()
    yield
    await close_mongo()



app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://192.168.1.2:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Welcom e to the Minimart API!"}

app.include_router(appinfo_router)
app.include_router(activity_router)
app.include_router(customer_routes)
app.include_router(product_routes)

