FROM python:3.11-slim-bullseye

WORKDIR /app

ENV DATABASE_URL=${DATABASE_URL}

COPY . . 

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]