from pydantic import BaseModel

class CreateProduct(BaseModel):

    name:str
    price:float
    status:bool
    category:str
    description:str