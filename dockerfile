FROM python:3.13-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.13-slim

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UVICORN_WORKERS=4 \
    UVICORN_TIMEOUT=120


EXPOSE 8443

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8443 --workers 4 ${SSL_OPTIONS}"]