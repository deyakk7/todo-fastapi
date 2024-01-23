from typing import Union, Annotated

from fastapi import Depends

from src.auth.dependencies import db_dependency
from src.todos.exc import invalid_todo_exc, not_a_owner_exc
from src.todos.models import Todo
from src.todos.schemas import TodoOut
from src.users.dependencies import user_dependency


def get_todo_by_id(db: db_dependency, todo_id: int, user: user_dependency) -> Todo:
    db_todo: TodoOut | Todo | None = db.query(Todo).filter(Todo.id == todo_id).first()

    if not db_todo:
        raise invalid_todo_exc

    if user.id != db_todo.owner_id:
        raise not_a_owner_exc

    return db_todo


todo_dependency = Annotated[TodoOut, Depends(get_todo_by_id)]
