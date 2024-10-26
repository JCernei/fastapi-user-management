from datetime import timedelta
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.cruds import user as crud
from app.database import get_db
from app.schemas import user as schemas
from app.utils import authentication as utils
from config import settings

router = APIRouter()

DBSession = Annotated[Session, Depends(get_db)]
Authenticated_User = Annotated[schemas.UserResponse, Depends(crud.get_current_user)]


@router.post("/register")
def register(user: schemas.UserCreate, db: DBSession):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists.",
        )

    db_user_by_username = crud.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(
            status_code=400,
            detail="This username is already taken.",
        )

    return schemas.UserResponse.model_validate(crud.create_user(db, user))


@router.post("/token", response_model=schemas.Token)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: DBSession
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get("", response_model=List[schemas.UserResponse])
async def read_users(db: DBSession):
    users = crud.get_users(db)
    return schemas.UserResponse.model_validate(users)


@router.get("/{id}", response_model=schemas.UserResponse)
async def read_user(
        id: int,
        current_user: Authenticated_User,
        db: DBSession
):
    db_user = crud.get_user(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserResponse.model_validate(db_user)


@router.put("/{id}", response_model=schemas.UserResponse)
async def update_user(
        id: int,
        user_update: schemas.UserUpdate,
        current_user: Authenticated_User,
        db: DBSession
):
    # Check if the current user is updating their own profile
    if id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update other users"
        )

    updated_user = crud.update_user(db, id=id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserResponse.model_validate(updated_user)


@router.delete("/{id}", response_model=schemas.UserResponse)
async def delete_user(
        id: int,
        current_user: Authenticated_User,
        db: DBSession
):
    # Check if the current user is deleting their own profile
    if id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete other users"
        )

    deleted_user = crud.delete_user(db, id=id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserResponse.model_validate(deleted_user)
