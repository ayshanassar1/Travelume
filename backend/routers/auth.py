from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import json
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.models import UserLogin, UserSignup, UserResponse, Token
from modules.database import get_database

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Configuration — SECRET_KEY MUST be set via environment variable
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    import warnings
    # Fallback for local dev only — generates a random key per process restart
    # This means all tokens are invalidated on every restart in dev.
    # In production, JWT_SECRET_KEY MUST be set in the environment.
    import secrets as _secrets
    SECRET_KEY = _secrets.token_hex(32)
    warnings.warn(
        "WARNING: JWT_SECRET_KEY is not set. A random key was generated — all tokens "
        "will be invalidated on every server restart. Set JWT_SECRET_KEY in your .env file.",
        stacklevel=2,
    )
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 hours — prevents silent 401s mid-session

# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_users():
    db = get_database()
    return db.users

def save_users(users):
    db = get_database()
    db.users = users
    db._save_json(db.users_file, users)

def verify_password(plain_password, hashed_password):
    # For now, we are supporting plain text legacy passwords from the streamlit app
    # In a real migration, we would hash them.
    # If the stored password doesn't look like a hash (e.g. too short), assume plain text
    if len(hashed_password) < 50: 
        return plain_password == hashed_password
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserSignup):
    users = get_users()
    if user.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Save user
    users[user.email] = {
        "name": user.name,
        "email": user.email,
        "password": get_password_hash(user.password),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_users(users)
    
    # Create token
    access_token = create_access_token(data={"sub": user.email})
    
    return UserResponse(name=user.name, email=user.email, token=access_token)

@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin):
    users = get_users()
    if user.email not in users:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    stored_user = users[user.email]
    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    
    return UserResponse(name=stored_user["name"], email=user.email, token=access_token)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to get the currently authenticated user from the JWT token.
    Raises 401 if token is invalid or missing.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    users = get_users()
    if email not in users:
        raise credentials_exception
    
    # Return user info (useful for routers)
    return {"email": email, "name": users[email].get("name")}

