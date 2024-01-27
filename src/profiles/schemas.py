from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    first_name: str | None = Field(min_length=5)
    last_name: str | None


class ProfileChange(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    user_id: int
    picture: str
