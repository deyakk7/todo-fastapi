from src.profiles.models import Profile
from fastapi import APIRouter


router = APIRouter(
    tags=['profiles'],
    prefix='/profiles'
)

