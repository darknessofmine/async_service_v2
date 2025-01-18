from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Path, status, UploadFile

from .services import SubTierService
from .schemas import SubTierCreate, SubTierResponse, SubTierUpdate
from api.auth.permissions import IsOwner, Permissions
from background_tasks.files.file_service import file_service
from core.models import User


router = APIRouter(
    prefix="/sub_tiers",
    tags=["sub_tiers"],
)


@router.post("/",
             response_model=SubTierResponse,
             status_code=status.HTTP_201_CREATED)
async def create_sub_tier(
    user: Annotated[User, Depends(Permissions("is_author"))],
    sub_tier_service: Annotated[SubTierService, Depends(SubTierService)],
    title: str = Form(...),
    text: str = Form(...),
    price: int = Form(...),
    image: Annotated[UploadFile | str | None, File()] = None,
) -> SubTierResponse:
    image_url = file_service.get_sub_tier_image_url(image)
    # TODO: Finish backgruond file save.
    file_service.save_file(image, image_url)
    sub_tier_create = SubTierCreate(
        title=title,
        text=text,
        price=price,
        image_url=image_url,
    )
    return await sub_tier_service.create_sub_tier(user, sub_tier_create)


@router.get("/{username}",
            response_model=list[SubTierResponse],
            status_code=status.HTTP_200_OK)
async def get_user_sub_tiers(
    sub_tier_service: Annotated[SubTierService, Depends(SubTierService)],
    username: Annotated[str, Path],
) -> list[SubTierResponse]:
    return await sub_tier_service.get_sub_tier_list_by_username(username)


@router.patch("/{sub_tier_id}",
              response_model=SubTierResponse,
              status_code=status.HTTP_200_OK)
async def update_sub_tier(
    user: Annotated[User, Depends(IsOwner("sub_tier"))],
    sub_tier_service: Annotated[SubTierService, Depends(SubTierService)],
    title: str | None = Form(None),
    text: str | None = Form(None),
    price: int | None = Form(None),
    image: Annotated[UploadFile | str | None, File()] = None,
) -> SubTierResponse:
    image_url = file_service.get_sub_tier_image_url(image)
    # TODO: Finish backgruond file save.
    file_service.save_file(image, image_url)
    sub_tier_update = SubTierUpdate(
        title=title,
        text=text,
        price=price,
        image_url=image_url,
    )
    return await sub_tier_service.update_sub_tier(
        sub_tier_update=sub_tier_update,
        sub_tier_id=user.sub_tiers[0].id
    )


@router.delete("/{sub_tier_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_sub_tier(
    user: Annotated[User, Depends(IsOwner("sub_tier"))],
    sub_tier_service: Annotated[SubTierService, Depends(SubTierService)],
) -> None:
    await sub_tier_service.delete_sub_tier(user.sub_tiers[0].id)
