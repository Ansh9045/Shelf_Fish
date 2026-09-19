from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Annotated, Sequence
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from database.database import get_session
from auth.auth import get_current_user
from auth.models import User
from .models import Detection, DetectionRead
from .detect import identify_product

router = APIRouter(prefix="/detections", tags=["detections"])

Session = Annotated[AsyncSession, Depends(get_session)]
currentUser = Annotated[User, Depends(get_current_user)]

@router.post("/", response_model=DetectionRead, status_code=status.HTTP_201_CREATED)
async def scan_product(
    session: Session,
    current_user: currentUser,
    file: UploadFile = File(...),
):
    if file.content_type != "image/jpeg":
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "Invalid file type. Only JPEG images are allowed."
        )
    
    img_bytes = await file.read()
    raw = await identify_product(img_bytes)
    detection = Detection( name = raw.name, brand = raw.brand, category = raw.category, user_id = current_user.id )

    session.add(detection)
    await session.commit()
    await session.refresh(detection)
    return detection

@router.get("/" , response_model=Sequence[DetectionRead], status_code=status.HTTP_200_OK)
async def list_detections(session:Session, current_user :currentUser):
    result = await session.exec(select(Detection).where(Detection.user_id == current_user.id))
    return result.all()