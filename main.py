from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import schedule, user, auth
from app.logging_conf.loger import setup_logging
from app.logging_conf.loging_middleware import log_requests
from app.core.config import load_config
import logfire

config = load_config()

logfire.configure()

app = FastAPI(debug=config.DEBUG)

logfire.instrument_fastapi(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://frontend.ru",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"], 
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    max_age=86400,  # Кешировать CORS-правила на 24 часа
)

setup_logging()

if config.ENABLE_LOGGING_MIDDLEWARE:
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