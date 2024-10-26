from sqlalchemy import Column, String

from app.database import Base
from app.models.mixins import BaseModelMixin


class User(Base, BaseModelMixin):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
