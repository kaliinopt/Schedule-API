from fastapi import Request
import logging
from datetime import datetime

logger = logging.getLogger("app")

async def log_requests(request: Request, call_next):
    """Middleware для логирования HTTP-запросов"""
    logger.info(f"Request: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
    except Exception as ex:
        logger.error(f"Error: {str(ex)}", exc_info=True)
        raise
    
    logger.info(
            f"Response: {request.method} {request.url} "
            f"- Status code: {response.status_code} "
        )
    
    return response