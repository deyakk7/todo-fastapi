import re
from datetime import timedelta, datetime

from fastapi import status, HTTPException
from jose import jwt, JWTError, ExpiredSignatureError

from src import settigns
from src.dependencies import db_dependency
from src.users import models


def get_user_by_email(db: db_dependency, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def password_validation(password: str):
    password_regex = r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"
    return re.match(password_regex, password)


def create_access_token(data: dict, expires_delta: timedelta):
    expire = datetime.utcnow() + expires_delta
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, settigns.SECRET_KEY, algorithm=settigns.ALGORYTHM)
    return encoded_jwt


def get_user_by_token(token: str, db: db_dependency):
    payload = decode_jwt(token)
    email = payload.get('sub')
    user = get_user_by_email(email=email, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No such use :Dr")
    return user


def verify_token(token: str, db: db_dependency):
    payload = decode_jwt(token)
    email = payload.get('sub')
    user = get_user_by_email(email=email, db=db)
    return bool(user)


def decode_jwt(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_jwt = jwt.decode(token, settigns.SECRET_KEY, algorithms=[settigns.ALGORYTHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="token has been expired")
    except JWTError:
        raise credentials_exception
    return decoded_jwt
