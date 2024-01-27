from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from src.settigns import DEFAULT_AVATAR_URL


class Profile(Base):
    __tablename__ = "profiles"

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    first_name: str = Column(String, nullable=True)
    last_name: str = Column(String, nullable=True)
    picture: str = Column(String, default=str(DEFAULT_AVATAR_URL))

    user_id: int = Column(ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="profile", uselist=False)
