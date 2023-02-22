from datetime import date
import os
from fastapi import APIRouter, Form, Header, UploadFile

from crud import AuthorRepository, BookRepository

import schemas

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get("/")
async def list_books(limit: int = 100) -> list[schemas.Book]:
    books = BookRepository().list(limit=limit)
    print(books)
    return books  # type: ignore


@router.get("/{book_id}")
async def retrieve_book(book_id: int) -> schemas.Book:
    return BookRepository().find(book_id)


@router.post("/")
async def create_book(
    image: UploadFile,
    title: str = Form(),
    release_date: str = Form(),
    number_of_pages: str = Form(),
    author_id: str = Form(),
) -> schemas.Book:
    author = AuthorRepository().find(int(author_id))
    upload_path = f"./uploads/{author.id}"
    os.makedirs(upload_path, exist_ok=True)
    image_path = upload_path + f"/{title}.jpg"
    with open(image_path, "wb") as upload:
        upload.write(image.file.read())

    release_date_split = [int(d) for d in release_date.split("-")]
    new_book = schemas.BookCreate(
        title=title,
        release_date=date(
            release_date_split[0], release_date_split[1], release_date_split[2]),
        number_of_pages=int(number_of_pages),
        author_id=int(author_id),
        image_url=f"/static/{author_id}/{title}.jpg")
    return BookRepository().create(new_book)


@ router.delete("/{book_id}")
async def delete_book(book_id: int) -> schemas.Book:
    return BookRepository().delete(book_id)
