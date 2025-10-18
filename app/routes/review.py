from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Laptop, Review
from database import get_db
from api_schemas.review import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/", tags=["Reviews"])

@router.post("/{laptop_id}", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(laptop_id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")

    new_review = Review(laptop_id=laptop_id, **review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.get("/{laptop_id}", response_model=list[ReviewResponse])
def get_reviews(laptop_id: int, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")

    reviews = db.query(Review).filter(Review.laptop_id == laptop_id).all()
    return reviews


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}
