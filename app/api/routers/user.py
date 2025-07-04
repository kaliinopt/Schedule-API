from . import schemas, models, utils, oath2
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from . import get_db
from sqlalchemy import select


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """Создание обычного пользователя, права есть только на просмотр"""
    result = await db.execute(
        select(models.User).where(models.User.username == user.username)
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    hashed_password = utils.hash(user.password)

    user.password = hashed_password

    new_user = models.User(**user.model_dump(), role="user")

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post(
    "/admin", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
async def create_admin(
    admin: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: models.User = Depends(oath2.require_role("admin")),
):
    """Создание новых админов, эндпоинт защищен от обычных пользователей,
    рекомендуется создать админа сразу в базе данных"""

    result = await db.execute(
        select(models.User).where(models.User.username == admin.username)
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    hashed_password = utils.hash(admin.password)

    admin.password = hashed_password

    new_user = models.User(**admin.model_dump(), role="admin")

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    """Получения пользователя по id, не факт, что может понадобиться"""
    result = await db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с id: {id} не существует",
        )

    return user
