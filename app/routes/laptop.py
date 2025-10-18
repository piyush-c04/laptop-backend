from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.laptop import Laptop
from database import get_db
from api_schemas import LaptopCreate
from app.utils.security import require_role


router = APIRouter()

@router.get("/laptops/")
def read_laptops(db: Session = Depends(get_db)):
    laptops = db.query(Laptop).all()
    return laptops

@router.get("/laptops/{laptop_id}")
def read_laptop(laptop_id: int, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return laptop


#only admins can create, update, delete laptops


@router.post("/create/laptops", status_code=status.HTTP_201_CREATED,dependencies=[Depends(require_role("admin"))])
def create_laptop(laptop: LaptopCreate, db: Session = Depends(get_db)):
    db.add(laptop)
    db.commit()
    db.refresh(laptop)
    return {"Laptop Created! : ", laptop}

@router.delete("/delete/laptops/{laptop_id}", status_code=status.HTTP_204_NO_CONTENT,dependencies=[Depends(require_role("admin"))])
def delete_laptop(laptop_id: int, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    deleted_id = laptop.id
    db.delete(laptop)
    db.commit()
    return {"Deleted Laptop ID": deleted_id}

@router.put("/update/laptops/{laptop_id}",dependencies=[Depends(require_role("admin"))])
def update_laptop(laptop_id: int, laptop_data: LaptopCreate, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    
    for key, value in laptop_data.dict().items():
        setattr(laptop, key, value)
    
    db.commit()
    db.refresh(laptop)
    return {"Updated Laptop : ", laptop}
