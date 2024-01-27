from fastapi import UploadFile

from src.settigns import UPLOAD_AVATAR


async def save_image(image: UploadFile, file_name: str):
    image = await image.read()

    path = f"/{UPLOAD_AVATAR}/{file_name}"

    with open(path, "wb") as f:
        f.write(image)
