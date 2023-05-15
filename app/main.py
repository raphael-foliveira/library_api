from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.authors import routes
from app.books import routes

app = FastAPI(responses={404: {"error": "not found"}})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./uploads"), name="uploads")

app.include_router(routes.router)
app.include_router(routes.get_author_router())
