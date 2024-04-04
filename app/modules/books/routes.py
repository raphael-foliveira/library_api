from fastapi import APIRouter, Depends, HTTPException

from app.modules.authors.models import AuthorModel

from ..authors.repository import AuthorRepository
from ..authors.routes import get_author_repository
from .providers import get_books_repository
from .repository import BookRepository
from .schemas import Book, BookDetails, CreateBook, book_details

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get("/", response_model=list[Book])
def list_books(repository: BookRepository = Depends(get_books_repository)):
    return repository.list()


@books_router.get("/{book_id}/", response_model=BookDetails)
def retrieve_book(
    book_id: int,
    repository: BookRepository = Depends(get_books_repository),
    author_repository: AuthorRepository = Depends(get_author_repository),
):
    book: Book | None = repository.find_one(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    author: AuthorModel | None = author_repository.find_one(book.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return book_details(book, author)


@books_router.post("/", status_code=201, response_model=Book)
async def create_book(
    book_schema: CreateBook,
    author_repository: AuthorRepository = Depends(get_author_repository),
    repository: BookRepository = Depends(get_books_repository),
):
    author_repository.find_one(int(book_schema.author_id))
    return repository.create(book_schema)


@books_router.delete("/{book_id}/", status_code=204)
def delete_book(
    book_id: int, repository: BookRepository = Depends(get_books_repository)
):
    ok = repository.delete(book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return ok
