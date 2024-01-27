from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    profile = relationship("Profile", back_populates='user', cascade="all, delete-orphan", uselist=False)
    todos = relationship("Todo", back_populates='owner', cascade="all, delete-orphan")
