from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models.User_model import User
from src.database import get_db
from src.utils.security import hash_password, verify_password
from src.api_schemas.user import UserCreate
from src.utils.security import create_access_token
from src.utils.security import logout_token
from fastapi import Header


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(email:str , password:str , db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Truncate the password to ensure it's no more than 72 bytes
    password_str = user.password  # Original password string
    encoded_password = password_str.encode('utf-8')  # Encode to bytes (UTF-8)
    
    if len(encoded_password) > 72:
        truncated_encoded = encoded_password[:72]  # Truncate to 72 bytes
        # Decode back to string (handle potential decoding errors)
        try:
            truncated_password = truncated_encoded.decode('utf-8')
        except UnicodeDecodeError:
            # If truncation results in invalid UTF-8, ignore errors or replace
            truncated_password = truncated_encoded.decode('utf-8', errors='replace')  # Or 'ignore'
    else:
        truncated_password = password_str  # No need to truncate
    
    # Now hash the truncated password
    hashed_password = hash_password(truncated_password)
    
    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,  # Use the truncated and hashed password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"name": new_user.first_name, "email": new_user.email}

blacklisted_tokens = set()  # you can replace this with Redis or DB

@router.post("/logout")
def logout(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    logout_token(token)
    return {"message": "Logged out successfully"}


