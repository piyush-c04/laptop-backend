from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_created = Column(String, nullable=False, default='now()')
    is_active = Column(String, default='true', nullable=False)
    role = Column(String, default="user")

    reviews = relationship("Review", back_populates="user", cascade="all, delete")
