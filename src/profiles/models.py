from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    first_name: str = Column(String)
    last_name: str = Column(String)
    picture: str = Column(String)

    user_id: int = Column(ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="profile", uselist=False)
