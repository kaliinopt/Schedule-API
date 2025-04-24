from fastapi import FastAPI, Request
from routers import schedule, user, auth
from logging_conf.loger import setup_logging
from logging_conf.loging_middleware import log_requests

app = FastAPI()

setup_logging()

@app.middleware("http")
async def loging_middelware(request: Request, call_next):
    return await log_requests(request, call_next)

#Проверка статуса
@app.get("/")
def root():
    return {"message": "OK"}

app.include_router(schedule.router)
app.include_router(auth.router)
app.include_router(user.router)