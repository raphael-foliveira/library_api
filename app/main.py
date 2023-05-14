from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import authors, books

app = FastAPI(responses={404: {"error": "not found"}})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./uploads"), name="uploads")

app.include_router(books.router)
app.include_router(authors.get_author_router())
