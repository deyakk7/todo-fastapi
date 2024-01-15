from fastapi import APIRouter

from src.auth.dependencies import db_dependency
from src.todos.dependencies import todo_dependency
from src.todos.models import Todo
from src.todos.schemas import TodoOut, TodoIn
from src.users.dependencies import user_dependency

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


@router.post('/', response_model=TodoOut)
async def create_todo(user: user_dependency, todo: TodoIn, db: db_dependency):
    db_todo = Todo(**todo.model_dump(), owner_id=user.id)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


@router.get('/my/', response_model=list[TodoOut])
async def get_all_todos_of_current_user(user: user_dependency):
    return user.todos


@router.get('/{todo_id}/', response_model=TodoOut)
async def get_todo(todo: todo_dependency):
    return todo


@router.put('/{todo_id}/', response_model=TodoOut)
async def change_todo(new_todo: TodoIn, todo: todo_dependency, db: db_dependency):
    todo.title = new_todo.title
    todo.description = new_todo.description

    db.commit()
    db.refresh(todo)

    return todo


@router.delete('/{todo_id}/')
async def delete_todo(todo: todo_dependency, db: db_dependency):
    db.delete(todo)
    db.commit()
    return {'message': "todo was deleted successfully"}
