from fastapi import APIRouter

admin_routes = APIRouter(
    prefix="admin",
    tags=["Admin Route"]
)

@admin_routes.post("/register")
def register_admin():
    return{"message":"Admin Created"}