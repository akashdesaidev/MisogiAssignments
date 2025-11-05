from fastapi import APIRouter
from DB import get_db

router = APIRouter()

@router.get("/admin")
async def admin_dashboard():
    return {"message": "Welcome to the Admin Dashboard"}

# post /admin/theatres route to create a theater
@router.post("/admin/theatres")
async def create_theater(theater: dict):
    # Logic to create a theater would go here
    return {"message": "Theater created successfully", "theater": theater}