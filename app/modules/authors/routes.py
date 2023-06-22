from fastapi import APIRouter
from sqlalchemy import Engine
from app.modules.authors.crud import AuthorRepository
from app.modules.authors.handlers import AuthorHandler
from app.database.config import engine


class AuthorsRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        handler = AuthorHandler(AuthorRepository(engine))
        self.add_api_route("/", handler.list_authors, methods=["GET"])
        self.add_api_route("/{author_id}/", handler.retrieve_author, methods=["GET"])
        self.add_api_route(
            "/", handler.create_author, methods=["POST"], status_code=201
        )
        self.add_api_route("/{author_id}/", handler.delete_author, methods=["DELETE"])
