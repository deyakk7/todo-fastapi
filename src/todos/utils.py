from src.auth.dependencies import db_dependency
from src.todos.exc import invalid_todo_exc
from src.todos.models import Todo
from src.todos.schemas import TodoOut


def get_todo_by_id(todo_id: int, db: db_dependency) -> TodoOut:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise invalid_todo_exc

    return todo
