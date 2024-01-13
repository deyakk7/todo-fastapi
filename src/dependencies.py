from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/login/access-token/')

db_dependency = Annotated[Session, Depends(get_db)]
token_dependency = Annotated[str, Depends(oauth2_scheme)]
