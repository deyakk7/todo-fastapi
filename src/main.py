from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from src.auth import router as auth_router
from src.database import Base, engine
from src.todos import router as todo_router
from src.users import router as user_router
from src.profiles import router as profile_router
import os
from src.settigns import UPLOAD_AVATAR

Base.metadata.create_all(bind=engine)

app = FastAPI()

router = APIRouter(prefix="/api/v1")

router.include_router(user_router.router)
router.include_router(todo_router.router)
router.include_router(auth_router.router)
router.include_router(profile_router.router)

app.include_router(router)


@app.get("/media/avatar/{image_name}/")
async def get_static_images(image_name: str):
    ls = os.listdir(UPLOAD_AVATAR)

    if image_name not in ls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No image")

    path = f'{UPLOAD_AVATAR}/{image_name}'
    return FileResponse(path)
