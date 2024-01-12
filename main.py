from fastapi import FastAPI, APIRouter

from db.engine import Base, engine
from routers import crud_users, auth, todos

Base.metadata.create_all(bind=engine)

app = FastAPI()

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(crud_users.router)
router.include_router(auth.router)
router.include_router(todos.router)

app.include_router(router)
