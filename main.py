from fastapi import FastAPI
import models
from database import sync_engine
from routers import schedule, user, auth

models.Base.metadata.create_all(bind=sync_engine)

app = FastAPI()


#Проверка статуса
@app.get("/")
async def root():
    return {"message": "OK"}
    
app.include_router(schedule.router)
app.include_router(auth.router)
app.include_router(user.router)