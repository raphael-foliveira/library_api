from datetime import date
import os
from fastapi import Depends, Form, HTTPException, Response, UploadFile
from app.modules.authors.crud import AuthorRepository, get_author_repository
from app.modules.books.crud import BookRepository
from . import schemas


def get_upload_path(authorId: str):
    return f"./uploads/{authorId}"


class BooksHandler:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def list_books(self) -> list[schemas.Book]:
        books = self.repository.list()
        return books

    async def retrieve_book(self, book_id: int) -> schemas.Book:
        try:
            return self.repository.find(book_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=e.args[0])

    async def create_book(
        self,
        image: UploadFile | None = None,
        title: str = Form(),
        release_date: str = Form(),
        number_of_pages: str = Form(),
        author_id: str = Form(),
        author_repository: AuthorRepository = Depends(get_author_repository),
    ) -> schemas.Book:
        try:
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

            return self.repository.create(new_book)
        except Exception as e:
            raise HTTPException(status_code=400, detail=e.args[1])

    async def delete_book(self, book_id: int) -> Response:
        if self.repository.delete(book_id):
            return Response(status_code=204)
        raise HTTPException(status_code=404, detail="Book not found")
