from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import User
from utils.auth import hash_password, verify_password, create_access_token

router = APIRouter()

# ── Request Models ──

class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    role: str = "faculty"  # "faculty" or "hod"

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# ── Endpoints ──

@router.post("/signup")
async def signup(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new faculty/HOD user."""
    
    # Check if user already exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "message": "User registered successfully!",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "role": db_user.role
        }
    }

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login and receive access token."""
    
    # Find user by email
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Create token
    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role}
    )
    
    return TokenResponse(
        access_token=access_token,
        user={
            "email": db_user.email,
            "name": db_user.name,
            "role": db_user.role
        }
    )