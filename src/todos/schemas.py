from pydantic import BaseModel, Field


class TodoIn(BaseModel):
    title: str = Field(min_length=1)
    description: str


class TodoOut(TodoIn):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
