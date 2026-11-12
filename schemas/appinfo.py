from pydantic import BaseModel

class AppInfo(BaseModel):
    name: str
    version: str
    description: str | None = None

class AppInfoCreate(AppInfo):
    name: str
    version: str
    description: str | None = None

class AppInfoUpdate(BaseModel):
    name: str | None = None
    version: str | None = None
    description: str | None = None

    

