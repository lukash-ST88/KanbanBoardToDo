from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from todo_app.db.database import Base
from sqlalchemy import ForeignKey, String, func, types



class Color(Base):
    __tablename__ = 'Color'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column()

    categories = relationship('Category', back_populates='color')
    themes = relationship('Theme', back_populates='color')

class Category(Base):
    __tablename__ = 'Category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    slug: Mapped[str] = mapped_column(String(30), unique=True)
    color_id: Mapped[int] = mapped_column(ForeignKey('Color.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id', ondelete='CASCADE'))

    color = relationship('Color', back_populates='categories')
    user = relationship('User', back_populates='categories')
    themes = relationship('Theme', back_populates='cat', cascade="all, delete", passive_deletes=True)

    def __str__(self):
        return self.name

#
#
class Theme(Base):
    __tablename__ = 'Theme'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    slug: Mapped[str] = mapped_column(String(30), unique=True)
    cat_id: Mapped[int] = mapped_column(ForeignKey('Category.id', ondelete='CASCADE'))
    color_id: Mapped[int] = mapped_column(ForeignKey('Color.id'))


    cat = relationship('Category', back_populates='themes')
    color = relationship('Color', back_populates='themes')
    tasks = relationship('Task', back_populates='theme', cascade="all, delete", passive_deletes=True)

    def __str__(self):
        return self.name
#
class Task(Base):
    __tablename__ = 'Task'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(30))
    slug: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    # date_created_timezone = mapped_column(types.DateTime(timezone=True), default=datetime.utcnow(), nullable=True)
    creation_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    update_date: Mapped[Optional[datetime]] = mapped_column(active_history=True, nullable=True)
    expiration_date: Mapped[Optional[datetime]] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)
    theme_id: Mapped[int] = mapped_column(ForeignKey('Theme.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id', ondelete='CASCADE'))

    theme = relationship('Theme', back_populates='tasks')
    user: Mapped['User'] = relationship(back_populates='tasks')

    def __str__(self):
        return self.title
