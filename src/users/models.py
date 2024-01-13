from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base
from src.todos.models import Todo


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    todos = relationship(Todo, back_populates='owner')
