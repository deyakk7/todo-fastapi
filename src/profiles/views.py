from typing import Annotated
from uuid import uuid4

from fastapi import UploadFile, Form, HTTPException
from pydantic import ValidationError
from starlette import status

from src.auth.dependencies import db_dependency
from src.profiles.models import Profile
from src.profiles.schemas import ProfileChange
from src.profiles.utils import save_image
from src.settigns import UPLOAD_AVATAR_URL
from src.users.dependencies import user_dependency


async def update_profile(
    user: user_dependency,
    image: UploadFile = None,
    first_name: Annotated[str, Form()] = None,
    last_name: Annotated[str, Form()] = None,

):
    profile = user.profile

    try:
        changed_profile = ProfileChange(first_name=first_name, last_name=last_name)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Validations error",
        )

    for key, value in changed_profile.model_dump().items():
        if value is not None:
            setattr(profile, key, value)

    if image is not None:
        file_name = f'{uuid4()}.jpg'
        await save_image(image, file_name)
        profile.picture = f"{UPLOAD_AVATAR_URL}{file_name}/"

    return profile


def create_profile(db: db_dependency, user_id: int):
    profile = Profile(user_id=user_id)

    db.add(profile)
    db.commit()
    db.refresh(profile)
