from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    SQLALCHEMY_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEBUG: bool

def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)  # Загружаем переменные окружения из файла .env

    return Config(
        SQLALCHEMY_DATABASE_URL=env("SQLALCHEMY_DATABASE_URL"),
        SECRET_KEY=env("SECRET_KEY"),
        ALGORITHM=env("ALGORITHM"),
        ACCESS_TOKEN_EXPIRE_MINUTES=env("ACCESS_TOKEN_EXPIRE_MINUTES"),
        DEBUG=env.bool("DEBUG", default=False)
    )

config = load_config()