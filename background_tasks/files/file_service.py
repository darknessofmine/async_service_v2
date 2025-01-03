import shutil

import aiofiles
from fastapi import UploadFile

from core.settings import BASE_DIR


class FileService:

    @staticmethod
    def save_file(file_to_save: UploadFile, file_url: str) -> None:
        with open(file_url, "wb") as new_file:
            shutil.copyfileobj(file_to_save.file, new_file)

    @staticmethod
    def get_profile_image_url(image: UploadFile) -> str | None:
        if image:
            return f"{BASE_DIR}/media/profile/{image.filename}"

    from asgiref.sync import async_to_sync

    @staticmethod
    async def save_file_async(file_to_save: UploadFile, file_url: str) -> None:
        async with aiofiles.open(file_url, "wb") as new_file:
            content = await file_to_save.read()
            await new_file.write(content)


file_service = FileService()
