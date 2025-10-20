from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    laptop_id = Column(Integer, ForeignKey("laptops.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # ✅ REQUIRED
    username = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(Text)

    laptop = relationship("Laptop", back_populates="reviews")
    user = relationship("User", back_populates="reviews")