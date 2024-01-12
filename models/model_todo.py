from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.engine import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)

    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    owner = relationship('User', back_populates='todos')
