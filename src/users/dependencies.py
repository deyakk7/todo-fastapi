from typing import Annotated

from fastapi import HTTPException, status, Depends

from src.auth.dependencies import token_dependency, db_dependency
from src.auth.exc import token_exc
from src.auth.utils import decode_jwt
from src.users.schemas import UserOut
from src.users.utils import get_user_by_email


def get_user_by_token(token: token_dependency, db: db_dependency):
    payload = decode_jwt(token)
    email = payload.get('sub')
    user = get_user_by_email(email=email, db=db)
    if not user:
        raise token_exc
    return user


user_dependency = Annotated[UserOut, Depends(get_user_by_token)]
