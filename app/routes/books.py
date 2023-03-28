import os
from datetime import date

from app import schemas
from app.crud.books import BookRepository
from app.crud.authors import AuthorRepository
from fastapi import APIRouter, Form, HTTPException, Response, UploadFile


router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get("/")
async def list_books() -> list[schemas.Book]:
    books = BookRepository().list()
    return books


@router.get("/{book_id}")
async def retrieve_book(book_id: int) -> schemas.Book:
    return BookRepository().find(book_id)


@router.post("/")
async def create_book(
    image: UploadFile | None,
    title: str = Form(),
    release_date: str = Form(),
    number_of_pages: str = Form(),
    author_id: str = Form(),
) -> schemas.Book:
    author = AuthorRepository().find(int(author_id))

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
        upload_path = f"./uploads/{author.id}"
        os.makedirs(upload_path, exist_ok=True)
        image_path = upload_path + f"/{title}.jpg"
        with open(image_path, "wb") as upload:
            upload.write(image.file.read())
        new_book.image_url = f"/static/{author_id}/{title}.jpg"

    return BookRepository().create(new_book)


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int) -> Response:
    if BookRepository().delete(book_id):
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Book not found")
