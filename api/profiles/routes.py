from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, status, UploadFile
from .schemas import ProfileResponse, ProfileUpdate
from .services import ProfileService
from api.auth.services import AuthService
# from background_tasks import tasks
from background_tasks.files.file_service import file_service
from core.models import User


router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


@router.get("/{username}",
            response_model=ProfileResponse,
            status_code=status.HTTP_200_OK)
async def get_user_profile(
    profile_service: Annotated[ProfileService, Depends(ProfileService)],
    username: str,
) -> ProfileResponse:
    return await profile_service.get_user_profile_by_username(username)


@router.patch("/update",
              response_model=ProfileResponse,
              status_code=status.HTTP_200_OK)
async def update_my_profile(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    profile_service: Annotated[ProfileService, Depends(ProfileService)],
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    bio: str | None = Form(None),
    image: Annotated[UploadFile | str | None, File()] = None,
):
    url = file_service.get_profile_image_url(image)
    profile_update = ProfileUpdate(
        first_name=first_name,
        last_name=last_name,
        bio=bio,
        image_url=url,
    )
    if image:
        file_service.save_file(image, url)
        # TODO: Finish backgruond file save.
        # tasks.save_profile_image.delay(image, url)
    return await profile_service.update_user_profile(
        user=current_user,
        profile_update=profile_update,
    )
