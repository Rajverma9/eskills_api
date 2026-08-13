from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.services.auth_service import hash_password,verify_password,create_access_token
from app.services.course_service import get_current_user

router = APIRouter(prefix="/auth",tags=["Auth"])

# Register
@router.post("/register")
def register(username: str,email: str,password: str,session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == email)).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    hashed_password = hash_password(password)
    user = User(username=username,email=email,hashed_password=hashed_password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "Registration successful"
    }

# Login
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),session: Session = Depends(get_session)):
    email = form_data.username
    password = form_data.password
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        raise HTTPException(status_code=401,detail="Invalid email or password")

    if not verify_password(password,user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user.username})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# Profile
@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email
    }