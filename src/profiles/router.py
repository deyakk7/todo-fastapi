from typing import Annotated

from fastapi import APIRouter, UploadFile, Form, File, HTTPException, status
from pydantic import ValidationError

from src.auth.dependencies import db_dependency
from src.profiles.models import Profile
from src.profiles.schemas import ProfileBase, ProfileChange, ProfileOut
from src.users.dependencies import user_dependency
from uuid import uuid4
from src.settigns import UPLOAD_AVATAR, UPLOAD_AVATAR_URL

router = APIRouter(tags=["profiles"], prefix="/profiles")


@router.get("/me/", response_model=ProfileOut)
async def get_current_profile(user: user_dependency):
    return user.profile


@router.put("/me/", response_model=ProfileOut)
async def change_current_profile(
    user: user_dependency,
    db: db_dependency,
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    file: UploadFile = File(...),
):
    profile = user.profile

    try:
        changed_profile = ProfileChange(first_name=first_name, last_name=last_name)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Validations error"
        )

    for key, value in changed_profile.model_dump().items():
        setattr(profile, key, value)

    file_name = f"{uuid4()}.jpg"

    image = await file.read()

    with open(f"{UPLOAD_AVATAR}/{file_name}", "wb") as f:
        f.write(image)

    profile.picture = f"{UPLOAD_AVATAR_URL}{file_name}/"

    db.add(profile)

    return profile

# TODO CLEAN ALL CODE
