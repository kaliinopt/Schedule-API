from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    TEST_DATABASE_URL: str
    SQLALCHEMY_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ENABLE_LOGGING_MIDDLEWARE: bool
    DEBUG: bool

def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)  # Загружаем переменные окружения из файла .env

    return Config(
        TEST_DATABASE_URL=env("TEST_DATABASE_URL"),
        SQLALCHEMY_DATABASE_URL=env("SQLALCHEMY_DATABASE_URL"),
        SECRET_KEY=env("SECRET_KEY"),
        ALGORITHM=env("ALGORITHM"),
        ACCESS_TOKEN_EXPIRE_MINUTES=env("ACCESS_TOKEN_EXPIRE_MINUTES"),
        ENABLE_LOGGING_MIDDLEWARE=env.bool("ENABLE_LOGGING_MIDDLEWARE"),
        DEBUG=env.bool("DEBUG")
    )

config = load_config()