from fastapi import APIRouter, HTTPException, status
from core.utils import get_user_by_token
from db.db import db_dependency, token_dependency
from models import model_todo
from schemas import schema_todo

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


@router.post('/', response_model=schema_todo.TodoOut)
async def create_todo(db: db_dependency, token: token_dependency, todo: schema_todo.Todo):
    user = get_user_by_token(token=token, db=db)
    db_todo = model_todo.Todo(**todo.model_dump(), owner_id=user.id)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


@router.get('/my/', response_model=list[schema_todo.TodoOut])
async def get_all_todos_of_current_user(db: db_dependency, token: token_dependency):
    user = get_user_by_token(token=token, db=db)
    return user.todos
