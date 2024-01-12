from pydantic import BaseModel, EmailStr, Field, field_validator

from core import utils
from schemas import schema_todo

password_regex = r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)

    @field_validator("password")
    def validate_password(cls, password):
        if not utils.password_validation(password):
            raise ValueError("Password is to week")
        return password


class UserOut(UserBase):
    id: int
    todos: list[schema_todo.Todo]


class UserCreateOut(UserBase):
    access_token: str


class User(UserOut):
    hashed_password: str

    class Config:
        from_attributes = True


class UserPassword(BaseModel):
    password: str


class UserPasswordChanging(UserPassword):
    new_password: str

    @field_validator("new_password")
    def validate_password(cls, password):
        if not utils.password_validation(password):
            raise ValueError("Password is to week")
        return password
