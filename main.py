from fastapi import FastAPI, Response, status, HTTPException, Depends
import models, schemas
from sqlalchemy.orm import Session
from database import get_db, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/api/schedule", response_model=List[schemas.ScheduleResponse])
def get_schedule(db: Session = Depends(get_db)):
    pass

@app.get("/api/schedule/{number}", response_model=schemas.ScheduleResponse)
def get_schedule_for_one_class(db: Session = Depends(get_db)):
    pass

@app.post("/schedule")
def create_schedule(db: Session = Depends(get_db)):
    pass
