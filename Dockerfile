FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860 \
    HOME=/tmp \
    CHAINLIT_APP_ROOT=/tmp

RUN pip install --upgrade pip && pip install \
    "chainlit>=2.11.1" \
    "openai>=1.30.0" \
    "openai-agents>=0.14.8" \
    "python-dotenv>=1.0.0" \
    "requests>=2.31.0"

COPY . .

EXPOSE 7860

CMD ["sh", "-c", "chainlit run main.py --host 0.0.0.0 --port ${PORT} --headless"]
