FROM python:3.11-slim-bullseye

WORKDIR /app

ENV DATABASE_URL=${DATABASE_URL}

COPY . . 

RUN pip install poetry && poetry install

EXPOSE 8000

CMD [ "poetry", "run", "uvicorn", "app.app:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]