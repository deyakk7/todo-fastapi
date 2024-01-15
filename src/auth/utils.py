from datetime import timedelta, datetime

from fastapi import HTTPException
from jose import jwt, ExpiredSignatureError, JWTError
from passlib import context

from src import settigns
from src.auth.dependencies import db_dependency
from src.auth.exc import credentials_exc
from src.users.utils import get_user_by_email

pwd_context = context.CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(current_password, hashed_password):
    return pwd_context.verify(current_password, hashed_password)


def verify_token(token: str, db: db_dependency):
    payload = decode_jwt(token)
    email = payload.get('sub')
    user = get_user_by_email(email=email, db=db)
    return bool(user)


def decode_jwt(token: str):
    try:
        decoded_jwt = jwt.decode(token, settigns.SECRET_KEY, algorithms=[settigns.ALGORYTHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="token has been expired")
    except JWTError:
        raise credentials_exc
    return decoded_jwt


def create_access_token(data: dict, expires_delta: timedelta):
    expire = datetime.utcnow() + expires_delta
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, settigns.SECRET_KEY, algorithm=settigns.ALGORYTHM)
    return encoded_jwt
#