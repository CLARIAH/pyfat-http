FROM python:3.12-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN apk add --no-cache openjdk11-jre-headless coreutils

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
