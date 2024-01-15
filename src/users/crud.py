from datetime import timedelta
from typing import List, Union

from fastapi import APIRouter, HTTPException, status

from src.auth.dependencies import db_dependency, token_dependency
from src.auth.exc import login_exc
from src.auth.utils import verify_token, create_access_token, get_hash_password, verify_password
from src.settigns import ACCESS_TOKEN_EXPIRES_DAY
from src.users.dependencies import user_dependency
from src.users.exc import email_in_use_exc, password_invalid_exc, password_to_week_exc
from src.users.models import User
from src.users.schemas import UserOut, UserCreateOut, UserCreate, UserPasswordChanging, UserPassword
from src.users.utils import get_user_by_email, password_validation

router = APIRouter(
    tags=['users'],
    prefix='/users'
)


@router.get('/', response_model=List[UserOut])
async def get_all_users(
        db: db_dependency,
        token: token_dependency,
        skip: Union[int, None] = 0,
        limit: Union[int, None] = 100
):
    if not verify_token(token=token, db=db):
        raise login_exc

    users = db.query(User).limit(limit=limit).offset(offset=skip).all()
    return users


@router.post('/', response_model=UserCreateOut)
async def create_user(user: UserCreate, db: db_dependency):
    if get_user_by_email(email=user.email, db=db):
        raise email_in_use_exc

    hashed_password = get_hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    data = {
        'sub': db_user.email,
        'user_id': db_user.id
    }
    expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRES_DAY)
    token = create_access_token(data=data, expires_delta=expires_delta)

    db_user.access_token = token

    return db_user


@router.get('/me/', response_model=UserOut)
async def get_current_user(user: user_dependency):
    return user


@router.post('/me/change-password/', response_model=UserOut)
async def change_password(user: user_dependency, form_data: UserPasswordChanging, db: db_dependency):
    password = form_data.password
    new_password = form_data.new_password

    if not verify_password(password, user.hashed_password):
        raise password_invalid_exc

    if not password_validation(new_password):
        raise password_to_week_exc

    user.hashed_password = get_hash_password(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.delete('/me/')
async def delete_user(user: user_dependency, form_data: UserPassword, db: db_dependency):
    db.delete(user)
    if not verify_password(form_data.password, user.hashed_password):
        raise password_invalid_exc

    db.commit()

    return {
        'message': "deleted successfully"
    }
