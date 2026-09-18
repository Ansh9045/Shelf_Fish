from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .database import get_session
from .models import Item, ItemCreate, ItemRead
from auth.auth import get_current_user
from auth.models import User

router = APIRouter(prefix="/items", tags=["items"])
Session = Annotated[AsyncSession, Depends(get_session)]

currentUser = Annotated[User, Depends(get_current_user)]

@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED )
async def create_item(item: ItemCreate, session: Session,current_user: currentUser):
    db_item = Item.model_validate(item, update={"owner_id": current_user.id})
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

@router.get("/", response_model=Sequence[ItemRead], status_code=status.HTTP_200_OK)
async def list_items(session: Session):
    result = await session.exec(select(Item))
    items =  result.all()
    return items

@router.get("/{item_id}", response_model = ItemRead, status_code = status.HTTP_200_OK)
async def get_item(item_id: int, session: Session):
    item = await session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@router.patch("/{item_id}", response_model = ItemRead, status_code = status.HTTP_200_OK)
async def update_item(item_id: int, item: ItemCreate, session: Session, current_user: currentUser):
    db_item = await session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, session: Session, current_user: currentUser):
    db_item = await session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Item not found")
    await session.delete(db_item)
    await session.commit()
    