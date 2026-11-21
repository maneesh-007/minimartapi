from fastapi import APIRouter,Depends,HTTPException,status
from utility import hash_password,create_uuid,verify_password,get_current_customer
from schemas.customer import RegisterCustomer,LoginCusstomer
from mydatabase import get_db
from sqlalchemy.orm import Session
from models.sql.customer import Customer


customer_routes = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)

@customer_routes.post("/generate_hash")
def generate_hash(plain_text:str):

    return hash_password(plain_text)

@customer_routes.post("/verify-hash")
def check_hash(plain_text:str,hash_text:str):

    if verify_password(plain_text,hash_text) :
        return{"message":"Hash Match"}

    return {"message":"Hash Dont Match"}




@customer_routes.post("/register", status_code=status.HTTP_201_CREATED)
def register_customer(customer: RegisterCustomer, db: Session = Depends(get_db)):
    # 1. Check if the email already exists
    usercheck = db.query(Customer).filter(Customer.email == customer.email).first()
    if usercheck:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email already taken"
        )
    
    # 2. Hash the password
    password_hashed = hash_password(customer.password)
    id = create_uuid()

    try:
        new_customer = Customer(
            first_name=customer.first_name,
            last_name=customer.last_name,
            phone_number=customer.phone,
            email=customer.email,
            password_hash=password_hashed
        )

        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

        return {"message": "Customer added successfully"}

    except Exception as e:
        db.rollback()  # Rollback the session to prevent it from staying in a broken state
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the customer."
        )


@customer_routes.post("/login")
def login_customer(user: LoginCusstomer, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email == user.email).first()

    if not customer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")

    if not verify_password(user.password, customer.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")

    # Generate JWT tokens (using email as 'sub')
    access_token = create_access_token(data={"sub": customer.email})
    refresh_token = create_refresh_token(data={"sub": customer.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@customer_routes.post("/refresh")
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if email is None or token_type != "refresh":
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    customer = db.query(Customer).filter(Customer.email == email).first()
    if not customer:
        raise credentials_exception

    # Issue a brand new access token
    new_access_token = create_access_token(data={"sub": customer.email})
    return {"access_token": new_access_token, "token_type": "bearer"}

@customer_routes.get("/me")
def get_logged_in_customer(current_customer: Customer = Depends(get_current_customer)):
    return {
        "id": current_customer.id,
        "email": current_customer.email,
        "first_name": current_customer.first_name,
        "last_name": current_customer.last_name
    }