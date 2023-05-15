from fastapi import APIRouter

from app.modules.books.handlers import BooksHandler

from app.modules.books.crud import BookRepository


def get_books_router():
    router = APIRouter(prefix="/books", tags=["books"])
    handler = BooksHandler(BookRepository())
    router.add_api_route("/", handler.list_books, methods=["GET"])
    router.add_api_route("/{book_id}/", handler.retrieve_book, methods=["GET"])
    router.add_api_route("/", handler.create_book, methods=["POST"], status_code=201)
    router.add_api_route("/{book_id}/", handler.delete_book, methods=["DELETE"])
    return router
