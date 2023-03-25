from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import books, authors
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(responses={404: {"error": "not found"}})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./uploads"), name="uploads")

app.include_router(books.routes.router)
app.include_router(authors.routes.router)
