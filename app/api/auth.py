from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import timedelta

from app.core.config import settings
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    verify_token
)
from app.db.mongodb import db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token, TokenPayload
from app.models.user import UserInDB

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token, settings.JWT_SECRET_KEY)
    if payload is None or payload.get("type") != "access":
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = await db.db.users.find_one({"email": email})
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate):
    # Check if user already exists
    if await db.db.users.find_one({"email": user_in.email}):
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    user_dict = UserInDB(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    ).model_dump()
    
    result = await db.db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict

@router.post("/login", response_model=Token)
async def login(user_in: UserLogin):
    user = await db.db.users.find_one({"email": user_in.email})
    if not user or not verify_password(user_in.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user["email"])
    refresh_token = create_refresh_token(subject=user["email"])
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token, settings.JWT_REFRESH_SECRET_KEY)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email = payload.get("sub")
    user = await db.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    new_access_token = create_access_token(subject=email)
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token, # Send back same or new refresh token
        "token_type": "bearer"
    }

@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "email": current_user["email"],
        "username": current_user["username"],
        "message": "This is a protected route!"
    }
