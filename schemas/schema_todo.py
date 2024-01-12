from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str = Field(min_length=1)
    description: str


class TodoOut(Todo):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
