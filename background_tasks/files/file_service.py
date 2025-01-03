import shutil

import aiofiles
from fastapi import UploadFile

from core.settings import BASE_DIR


class FileService:

    @staticmethod
    def save_file(file_to_save: UploadFile | str | None,
                  file_url: str) -> None:
        if file_to_save:
            with open(file_url, "wb") as new_file:
                shutil.copyfileobj(file_to_save.file, new_file)

    @staticmethod
    def get_profile_image_url(image: UploadFile | str | None) -> str | None:
        if image:
            return f"{BASE_DIR}/media/profile/{image.filename}"

    @staticmethod
    async def save_file_async(file_to_save: UploadFile | str | None,
                              file_url: str) -> None:
        if file_to_save:
            async with aiofiles.open(file_url, "wb") as new_file:
                content = await file_to_save.read()
                await new_file.write(content)


file_service = FileService()
