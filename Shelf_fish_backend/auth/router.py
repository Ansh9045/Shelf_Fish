from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from auth.models import User, UserCreate, UserRead, Token
from auth.auth import hash_password, verify_password, create_access_token
from database.database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])
Session = Annotated[AsyncSession, Depends(get_session)]

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, session: Session):
    existing_user = await session.exec(select(User).where((User.username == user_in.username) | (User.email == user_in.email)))
    if existing_user.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")

    user = User(
        username= user_in.username,
        email = user_in.email,
        full_name = user_in.full_name,
        hashed = hash_password(user_in.password)
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.post("/login", response_model=Token, status_code = status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session):
    result = await session.exec(select(User).where(User.username == form_data.username))
    user = result.first()

    if not user or not verify_password(form_data.password, user.hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token)

    