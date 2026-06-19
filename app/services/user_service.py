from fastapi import HTTPException

from app.crud.user import (
    create_user,
    get_user,
    delete_user,
    get_user_by_email
)


def create_user_service(db, user):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return create_user(
        db,
        user
    )


def get_user_service(
    db,
    user_id
):
    user = get_user(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


def delete_user_service(
    db,
    user_id
):
    user = delete_user(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }