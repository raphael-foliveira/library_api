import os
from datetime import date

from fastapi import APIRouter, Depends, Form, Response, UploadFile
from sqlalchemy.orm.session import Session

from app.database.config import get_db
from app.modules.authors.repository import AuthorRepository
from app.modules.authors.routes import get_author_repository
from app.modules.books import schemas
from app.modules.books.repository import BookRepository

books_router = APIRouter(prefix="/books", tags=["books"])


def get_upload_path(authorId: str):
    return f"./uploads/{authorId}"


def get_books_repository(db: Session = Depends(get_db)):
    return BookRepository(db)


@books_router.get("/")
def list_books(repository: BookRepository = Depends(get_books_repository)):
    return repository.list()


@books_router.get("/{book_id}/")
def retrieve_book(
    book_id: int, repository: BookRepository = Depends(get_books_repository)
):
    return repository.find(book_id)


@books_router.post("/", status_code=201)
async def create_book(
    image: UploadFile | None = None,
    title: str = Form(),
    release_date: str = Form(),
    number_of_pages: str = Form(),
    author_id: str = Form(),
    author_repository: AuthorRepository = Depends(get_author_repository),
    repository: BookRepository = Depends(get_books_repository),
) -> schemas.Book:
    author_repository.find(int(author_id))

    release_date_split = [int(d) for d in release_date.split("-")]
    new_book = schemas.BookCreate(
        title=title,
        release_date=date(
            release_date_split[0], release_date_split[1], release_date_split[2]
        ),
        number_of_pages=int(number_of_pages),
        author_id=int(author_id),
    )
    if image is not None:
        upload_path = get_upload_path(author_id)
        os.makedirs(upload_path, exist_ok=True)
        image_path = upload_path + f"/{title}.jpg"
        with open(image_path, "wb") as upload:
            upload.write(image.file.read())
        new_book.image_url = f"/static/{author_id}/{title}.jpg"

    return repository.create(new_book)


@books_router.delete("/{book_id}/")
def delete_book(
    book_id: int, repository: BookRepository = Depends(get_books_repository)
):
    repository.delete(book_id)
    return Response(status_code=204)
