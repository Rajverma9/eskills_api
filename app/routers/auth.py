import os
from dotenv import load_dotenv
from fastapi import APIRouter,Depends,HTTPException,Header
from jose import JWTError, jwt
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.services.course_service import get_current_user


load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM","HS256")

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register")
def register(username: str,email: str,password: str,session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=409,detail="Username or email already exists")
    user = User(email=email, hashed_password= hash_password(password))
    session.add(user)
    session.commit()
    return {"message": "User registered successfully","username": user.username,"email": user.email}


@router.post("/login")
def login(username: str,password: str,session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401,detail="Invalid username or password")
    token = create_access_token(user.username)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}