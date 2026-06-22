from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import user as crud_user
from app.schemas.user import UserCreate

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        if crud_user.get_user_by_email(db, user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        return crud_user.create_user(db, user_data)

    @staticmethod
    def get_user(db: Session, user_id: int):
        user = crud_user.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserService.get_user(db, user_id)
        crud_user.delete_user(db, user)
        return {"message": f"User {user_id} and all related data successfully deleted"}