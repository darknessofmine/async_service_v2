from fastapi import HTTPException, status


def client_is_not_sub_owner_or_403(
    client_id: int,
    owner_id: int,
) -> None:
    if owner_id == client_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't subscribe/unsubscribe yourself.",
        )
