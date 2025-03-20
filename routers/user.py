import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import select

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
   
    hashed_password = utils.hash(user.password)

    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id: {id} does not exist')
    
    return user