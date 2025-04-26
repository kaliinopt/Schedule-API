from fastapi import FastAPI, Request
from app.api.routers import schedule, user, auth
from app.logging_conf.loger import setup_logging
from app.logging_conf.loging_middleware import log_requests
from app.core.config import load_config

app = FastAPI()

config = load_config()

if config.DEBUG:
    app.debug = True
else:
    app.debug = False

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