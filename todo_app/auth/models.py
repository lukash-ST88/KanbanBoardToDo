from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from todo_app.db.database import Base
from sqlalchemy import String

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=30))

    categories = relationship('Category', back_populates='user', cascade="all, delete", passive_deletes=True)
    tasks = relationship('Task', back_populates='user', cascade="all, delete", passive_deletes=True)
