from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType


class BaseModelMixin:
    """Mixin for common model attributes"""

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
