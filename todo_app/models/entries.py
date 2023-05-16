from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from todo_app.db.database import Base
from sqlalchemy import ForeignKey, String, func, types



class Color(Base):
    __tablename__ = 'Color'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column()

    categories = relationship('Category', back_populates='color')
    themes = relationship('Theme', back_populates='color')

class Category(Base):
    __tablename__ = 'Category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    slug: Mapped[str] = mapped_column(String(30), unique=True, nullable=True) # delete nullable
    color_id: Mapped[int] = mapped_column(ForeignKey('Color.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id', ondelete='CASCADE'))

    color = relationship('Color', back_populates='categories')
    user = relationship('User', back_populates='categories')
    themes = relationship('Theme', back_populates='cat', cascade="all, delete", passive_deletes=True)

#
#
class Theme(Base):
    __tablename__ = 'Theme'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    slug: Mapped[str] = mapped_column(String(30), unique=True, nullable=True)  # delete nullable
    cat_id: Mapped[int] = mapped_column(ForeignKey('Category.id', ondelete='CASCADE'))
    color_id: Mapped[int] = mapped_column(ForeignKey('Color.id'))
    ## user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))

    cat = relationship('Category', back_populates='themes')
    color = relationship('Color', back_populates='themes')
    ## user: Mapped["User"] = relationship(back_populates='themes')
    tasks = relationship('Task', back_populates='theme', cascade="all, delete", passive_deletes=True)

#
class Task(Base):
    __tablename__ = 'Task'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    slug: Mapped[str] = mapped_column(String(30), unique=True, nullable=True)  # delete nullable
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    date_created_timezone = mapped_column(types.DateTime(timezone=True), default=datetime.utcnow(), nullable=True)
    date_created: Mapped[datetime] = mapped_column(insert_default=func.now())
    date_updated: Mapped[Optional[datetime]] = mapped_column(active_history=True, nullable=True)
    date_expiration: Mapped[Optional[datetime]] = mapped_column(default=func.now())
    completed: Mapped[bool] = mapped_column(default=False)
    theme_id: Mapped[int] = mapped_column(ForeignKey('Theme.id', ondelete='CASCADE'))
    # cat_id: Mapped[int] = mapped_column(ForeignKey('Category.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id', ondelete='CASCADE'))

    theme = relationship('Theme', back_populates='tasks')
    # cat: Mapped['Category'] = relationship(back_populates='tasks')
    user: Mapped['User'] = relationship(back_populates='tasks')
