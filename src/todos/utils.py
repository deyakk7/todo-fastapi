from fastapi import HTTPException, status

from src.auth.dependencies import db_dependency
from src.todos.models import Todo
from src.todos.schemas import TodoOut


def get_todo_by_id(todo_id: int, db: db_dependency) -> TodoOut:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No such todo with this id')

    return todo

#TODO THINK ABOUT SERVICES IN FOLDERS WITH BUSSINES LOGICS