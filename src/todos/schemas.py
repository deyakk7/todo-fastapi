from pydantic import BaseModel, Field


class TodoIn(BaseModel):
    title: str = Field(min_length=1)
    description: str


class TodoChange(TodoIn):
    completed: bool


class TodoOut(TodoChange):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
