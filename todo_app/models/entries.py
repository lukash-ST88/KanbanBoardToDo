from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from todo_app.db.database import Base
from sqlalchemy import ForeignKey, DATETIME


class Color(Base):
    __tablename__ = 'Color'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column()  # restriction to start with #312331

    categories: Mapped[List['Category']] = relationship(back_populates='color')
    themes: Mapped[List['Theme']] = relationship(back_populates='color')


class Category(Base):
    __tablename__ = 'Category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  # add max length
    color_id: Mapped[int] = mapped_column(ForeignKey('Color.id'))  # or color
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))

    color: Mapped["Color"] = relationship(back_populates='categories')
    user: Mapped["User"] = relationship(back_populates='categories')
    themes: Mapped[List['Theme']] = relationship(back_populates='cat')
    tasks: Mapped['Task'] = relationship(back_populates='cat')

class Theme(Base):
    __tablename__ = 'Theme'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  # add max length
    cat_id: Mapped[int] = mapped_column(ForeignKey('Category.id'))
    color_id: Mapped[int] = mapped_column(ForeignKey('Color.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))

    cat: Mapped["Category"] = relationship(back_populates='themes')
    color: Mapped["Color"] = relationship(back_populates='themes')
    user: Mapped["User"] = relationship(back_populates='themes')
    tasks: Mapped['Task'] = relationship(back_populates='theme')

class Task(Base):
    __tablename__ = mapped_column(primary_key=True)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] #  add max length
    description: Mapped[str] = mapped_column(nullable=True)
    # date_created: Mapped[DATETIME] = mapped_column()
    # date_exparation: Mapped[DATETIME]
    completed: Mapped[bool] = mapped_column(default=False)

    theme_id: Mapped[int] = mapped_column(ForeignKey('Theme.id'))
    cat_id: Mapped[int] = mapped_column(ForeignKey('Category.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))

    theme: Mapped['Theme'] = relationship(back_populates='tasks')
    cat: Mapped['Category'] = relationship(back_populates='tasks')
    user: Mapped['User'] = relationship(back_populates='tasks')