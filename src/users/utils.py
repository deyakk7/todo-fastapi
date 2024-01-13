import re

from src.auth.dependencies import db_dependency
from src.users import models


def get_user_by_email(db: db_dependency, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def password_validation(password: str):
    password_regex = r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"
    return re.match(password_regex, password)
