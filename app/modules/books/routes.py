from fastapi import APIRouter
from sqlalchemy import Engine
from app.modules.books.handlers import BooksHandler
from app.modules.books.crud import BookRepository
from app.database.config import engine


class BooksRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        handler = BooksHandler(BookRepository(engine))
        self.add_api_route("/", handler.list_books, methods=["GET"])
        self.add_api_route("/{book_id}/", handler.retrieve_book, methods=["GET"])
        self.add_api_route("/", handler.create_book, methods=["POST"], status_code=201)
        self.add_api_route("/{book_id}/", handler.delete_book, methods=["DELETE"])
