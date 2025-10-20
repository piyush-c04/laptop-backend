from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models.Laptop_model import Laptop
from src.database import get_db
from src.api_schemas.laptop import LaptopCreate, LaptopResponse
from src.api_schemas.review import ReviewCreate, ReviewResponse
from src.utils.security import require_role
from sqlalchemy import func
from typing import List

router = APIRouter(tags=["Laptops"])


@router.get("/", response_model=List[LaptopResponse])
def read_laptops(
    brand: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort_by: str | None = "price",
    db: Session = Depends(get_db)
):
    query = db.query(Laptop)

    if brand:
        query = query.filter(Laptop.brand == brand)
    if min_price:
        query = query.filter(Laptop.price >= min_price)
    if max_price:
        query = query.filter(Laptop.price <= max_price)
    if sort_by:
        query = query.order_by(getattr(Laptop, sort_by))

    laptops = query.all()  # ✅ fetch results at the end
    return laptops


@router.get("/",dependencies=[Depends(require_role("admin"))])
def read_laptops(db: Session = Depends(get_db)):
    laptops = db.query(Laptop).all()
    return laptops

@router.get("/{laptop_id}",response_model=LaptopResponse)
def read_laptop(laptop_id: int, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")

    return laptop


#only admins can create, update, delete laptops


@router.post("/create", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_role("admin"))])
def create_laptop(laptop: LaptopCreate, db: Session = Depends(get_db)):
    db.add(**laptop.model_dump())
    db.commit()
    db.refresh(laptop)
    return {"message": "Laptop Created!", "data": laptop}

@router.delete("/delete/{laptop_id}", status_code=status.HTTP_204_NO_CONTENT,dependencies=[Depends(require_role("admin"))])
def delete_laptop(laptop_id: int, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    deleted_id = laptop.id
    db.delete(laptop)
    db.commit()
    return {"Deleted Laptop ID": deleted_id}

@router.put("/update/{laptop_id}",dependencies=[Depends(require_role("admin"))])
def update_laptop(laptop_id: int, laptop_data: LaptopCreate, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    
    for key, value in laptop_data.model_dump().items():
        setattr(laptop, key, value)
    
    db.commit()
    db.refresh(laptop)
    return {"updated_laptop": laptop}


