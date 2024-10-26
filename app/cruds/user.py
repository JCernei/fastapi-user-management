from typing import Annotated
from uuid import UUID, uuid4

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import user as models
from app.schemas import user as schemas
from app.utils import authentication as utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token", scheme_name="JWT")


def create_user(db: Session, user: schemas.UserCreate):
    user_obj = models.User(
        # id=uuid4(),
        email=user.email,
        username=user.username,
        password_hash=utils.hash_password(user.password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not utils.verify_password(password, user.password_hash):
        return False
    return user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, id: UUID):
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"}, )

    try:
        payload = utils.decode_token(token)
        valid_payload = utils.validate_token(payload)
        user_id = valid_payload.get("sub")
    except JWTError:
        raise credentials_exception

    user = get_user(db, user_id)
    if user is None:
        raise credentials_exception

    return user


def update_user(db: Session, id: UUID, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = utils.hash_password(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, id: UUID):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user
