from fastapi import FastAPI, APIRouter

from src.auth import router as auth_router
from src.database import Base, engine
from src.todos import router as todo_router
from src.users import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(user_router.router)
router.include_router(todo_router.router)
router.include_router(auth_router.router)

app.include_router(router)
