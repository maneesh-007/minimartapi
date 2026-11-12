from fastapi import APIRouter
from utility import hash_password,verify_pasword

customer_routes = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)

@customer_routes.post("/generate_hash")
def generate_hash(plain_text:str):

    return hash_password(plain_text)

@customer_routes.post("/verify-hash")
def check_hash(plain_text:str,hash_text:str):

    if verify_pasword(plain_text,hash_text) :
        return{"message":"Hash Match"}

    return {"message":"Hash Dont Match"}