from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependencies import db_dependency
from src.profiles.models import Profile
from src.profiles.schemas import ProfileOut
from src.profiles.views import update_profile
from src.users.dependencies import user_dependency

router = APIRouter(tags=["profiles"], prefix="/profiles")


@router.get("/me/", response_model=ProfileOut)
async def get_current_profile(user: user_dependency):
    return user.profile


@router.patch("/me/", response_model=ProfileOut)
async def change_current_profile(
    profile: Annotated[Profile, Depends(update_profile)],
    db: db_dependency,
):
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/{profile_id}/", response_model=ProfileOut)
def get_profile_by_id(profile_id: int, db: db_dependency):
    profile = db.query(Profile).get(profile_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such profile with this id"
        )
    return profile
