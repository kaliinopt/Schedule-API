import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging():
    """Настройка базового логирования"""
    # Создаем папку для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s in %(module)s: %(message)s'
    )
    # 1. Логирование Uvicorn
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)
    
    # 2. Логирование приложения
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO)
    
    # Обработчик для файла (ротация по 5 МБ)
    file_handler = RotatingFileHandler(
        log_dir / "api.log",
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Добавляем обработчики
    for logger in [uvicorn_logger, app_logger]:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)