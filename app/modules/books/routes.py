from datetime import date
import os
from fastapi import APIRouter, Depends, Form, HTTPException, Response, UploadFile
from app.modules.authors.crud import AuthorRepository, get_author_repository
from app.modules.books import schemas
from app.modules.books.handlers import get_upload_path
from app.modules.books.crud import BookRepository, get_book_repository


books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get("/")
def list_books(repository: BookRepository = Depends(get_book_repository)):
    return repository.list()


@books_router.get("/{book_id}/")
def retrieve_book(
    book_id: int, repository: BookRepository = Depends(get_book_repository)
):
    try:
        return repository.find(book_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@books_router.post("/")
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


@books_router.delete("/{book_id}/")
def delete_book(
    book_id: int, repository: BookRepository = Depends(get_book_repository)
):
    if repository.delete(book_id):
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Book not found")
