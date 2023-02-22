from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import author, book


app = FastAPI(
    responses={404: {"error": "not found"}}
)

# Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount('/static', StaticFiles(directory='./uploads'), name='uploads')


app.include_router(author.router)
app.include_router(book.router)
