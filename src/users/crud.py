from datetime import timedelta
from typing import List

from fastapi import APIRouter, HTTPException, status

from src.dependencies import db_dependency, token_dependency
from src.security import get_hash_password, verify_password
from src.settigns import ACCESS_TOKEN_EXPIRES_DAY
from src.users.models import User
from src.users.schemas import UserOut, UserCreateOut, UserCreate, UserPasswordChanging, UserPassword
from src.users.utils import get_user_by_email, get_user_by_token, create_access_token
from src.users.utils import password_validation

router = APIRouter(
    tags=['users'],
    prefix='/users'
)


@router.get('/', response_model=List[UserOut])
async def get_all_users(db: db_dependency, token: token_dependency):
    if not get_user_by_token(token=token, db=db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    users = db.query(User).all()
    return users


@router.post('/', response_model=UserCreateOut)
async def create_user(user: UserCreate, db: db_dependency):
    if get_user_by_email(email=user.email, db=db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use!")

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
async def get_current_user(db: db_dependency, token: token_dependency):
    user = get_user_by_token(token=token, db=db)
    return user


@router.post('/me/change-password/', response_model=UserOut)
async def change_password(db: db_dependency, token: token_dependency, form_data: UserPasswordChanging):
    user = get_user_by_token(token=token, db=db)

    password = form_data.password
    new_password = form_data.new_password

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong current password")

    if not password_validation(new_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password to week!")

    user.hashed_password = get_hash_password(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.delete('/me/')
async def delete_user(db: db_dependency, token: token_dependency, form_data: UserPassword):
    user = get_user_by_token(db=db, token=token)
    db_user = db.delete(user)
    print(db_user)
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")

    db.commit()

    return {
        'message': "deleted successfully"
    }
