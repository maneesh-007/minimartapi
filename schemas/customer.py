from pydantic import BaseModel, Field, EmailStr

class RegisterCustomer(BaseModel):
    first_name: str = Field(..., max_length=30)
    last_name: str = Field(..., max_length=30)
    password: str = Field(..., min_length=8)  # Good practice to set a minimum password length
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=10,pattern=r"^\d{10}$")  # Ensures an exact 10-digit phone number


class LoginCusstomer(BaseModel):

    email:EmailStr
    password:str

    