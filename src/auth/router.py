from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from src import settigns
from src.auth.dependencies import db_dependency
from src.auth.utils import create_access_token, verify_password
from src.users import utils

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/login/access-token/')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = utils.get_user_by_email(email=form_data.username, db=db)
    if not user:
        raise HTTPException(status_code=404, detail='Bad data :D')

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong email or password")

    access_token_expires = timedelta(days=settigns.ACCESS_TOKEN_EXPIRES_DAY)
    access_token = create_access_token(
        data={
            'sub': user.email,
            'user_id': user.id,
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
