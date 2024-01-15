from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src import settigns
from src.auth.dependencies import db_dependency
from src.auth.exc import login_exc
from src.auth.utils import create_access_token, verify_password
from src.users.utils import get_user_by_email

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/login/access-token/')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = get_user_by_email(email=form_data.username, db=db)
    if not user:
        raise login_exc

    if not verify_password(form_data.password, user.hashed_password):
        raise login_exc

    access_token_expires = timedelta(days=settigns.ACCESS_TOKEN_EXPIRES_DAY)
    access_token = create_access_token(
        data={
            'sub': user.email,
            'user_id': user.id,
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
