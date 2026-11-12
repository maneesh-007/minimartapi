from fastapi import APIRouter,Depends
from models.sql import AppInfo
from mydatabase import get_db
from schemas.appinfo import AppInfoCreate
from sqlalchemy.orm import Session
appinfo_router = APIRouter(prefix="/appinfo", tags=["App Info"])

@appinfo_router.get("/")
async def get_app_info():
    return {"message": "App info goes here"}

@appinfo_router.post("/add")
def add_app_info(appinfo:AppInfoCreate,db:Session = Depends(get_db)):

    info = AppInfo(name=appinfo.name,version=appinfo.version,description=appinfo.description )


    db.add(info)
    db.commit()

    db.refresh(info)

    return{"app_info":info}
