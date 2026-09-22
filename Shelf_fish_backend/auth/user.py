from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from auth.auth import get_current_user
from auth.models import User, UserRead

router = APIRouter(prefix="/users", tags=["users"])
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get('/me', response_model=UserRead, status_code=status.HTTP_200_OK)
async def read_user(user: CurrentUser):
    return user

