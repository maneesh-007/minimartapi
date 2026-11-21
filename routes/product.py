from models.nosql.product import Product
from schemas.product import CreateProduct
from models.nosql.category import Category
from pathlib import Path
from typing import Optional
import os
from utility import create_uuid
import boto3
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
S3_BUCKET = os.getenv("S3_BUCKET", "products-bucket")
S3_REGION = os.getenv("S3_REGION", "us-east-1")
LOCAL_S3_DIR = Path(os.path.expanduser("~")) / "Downloads" / "S3"

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    region_name=S3_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
)

product_routes = APIRouter(
    prefix="/product",
    tags=["Product Route"]
)

@product_routes.post("/add")
async def add_product(
    name: str = Form(...),
    price: float = Form(...),
    originalPrice: float = Form(0.0),
    category: str = Form(""),
    status: bool = Form(...),
    rating: float = Form(0.0),
    reviews: int = Form(0),
    badge: str = Form(""),
    description: str = Form(""),
    image: Optional[UploadFile] = File(None),
):
    image_url = ""

    img_uuid = create_uuid()

    if image and image.filename:
        ext = Path(image.filename).suffix.lower()
        object_key = f"products/{img_uuid}{ext}"
        content = await image.read()

        try:
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=object_key,
                Body=content,
                ContentType=image.content_type or "application/octet-stream",
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"S3 upload failed: {exc}")

        local_file_path = LOCAL_S3_DIR / object_key
        local_file_path.parent.mkdir(parents=True, exist_ok=True)
        local_file_path.write_bytes(content)

        image_url = f"{S3_ENDPOINT_URL}/{S3_BUCKET}/{object_key}"

    new_product = Product(
        name=name,
        price=price,
        status=status,
        description=description,
        originalPrice=originalPrice,
        category=category,
        rating=rating,
        reviews=reviews,
        badge=badge,
        image=image_url,
    )

    await new_product.insert()
    return new_product


@product_routes.get("/all-products")
async def all_products():
    page = "Home"

    return await Product.find_all().sort('-created_at').to_list()

@product_routes.post("/category-add")
async def add_category(name: str = Form(...)
 ):

    new_category = Category(name = name)

    await new_category.insert()

    return new_category

    

@product_routes.get("/all-category")
async def all_categories():

   return await Category.find_all().to_list()