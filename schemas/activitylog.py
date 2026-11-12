from pydantic import BaseModel

class CreateActivity(BaseModel):
    action:str
    performed_by:str
    