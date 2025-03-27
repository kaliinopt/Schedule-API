import models, schemas, oath2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from typing import List

router = APIRouter(
    prefix="/api/schedule",
    tags=["Schedule"]
)

@router.get("/", response_model=List[schemas.ScheduleResponse])
async def get_schedule(db: AsyncSession = Depends(get_db)):
    pass

@router.get("/{number}", response_model=schemas.ScheduleResponse)
async def get_schedule_for_one_class(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(oath2.require_role("admin"))):
    
    
    
    pass

@router.post("/")
async def create_schedule(
    db: AsyncSession = Depends(get_db), 
    admin: models.User = Depends(oath2.require_role("admin"))):
    pass

@router.put("/")
async def create_schedule(
    db: AsyncSession = Depends(get_db), 
    admin: models.User = Depends(oath2.require_role("admin"))):
    
    pass

@router.delete("/")
async def create_schedule(
    db: AsyncSession = Depends(get_db), 
    current_user: models.User = Depends(oath2.require_role("admin"))):
    
    
    
    pass