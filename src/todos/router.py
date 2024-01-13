from fastapi import APIRouter

from src.todos.schemas import TodoOut
from src.users.utils import get_user_by_token
from src.dependencies import db_dependency, token_dependency
from src.todos import models, schemas

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


@router.post('/', response_model=TodoOut)
async def create_todo(db: db_dependency, token: token_dependency, todo: schemas.Todo):
    user = get_user_by_token(token=token, db=db)
    db_todo = schemas.Todo(**todo.model_dump(), owner_id=user.id)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


@router.get('/my/', response_model=list[TodoOut])
async def get_all_todos_of_current_user(db: db_dependency, token: token_dependency):
    user = get_user_by_token(token=token, db=db)
    return user.todos
