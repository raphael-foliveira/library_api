from fastapi import APIRouter
from app.modules.authors.crud import AuthorRepository
from app.modules.authors.handlers import AuthorHandler


def get_author_router():
    router = APIRouter(prefix="/authors", tags=["authors"])
    handler = AuthorHandler(AuthorRepository())

    router.add_api_route("/", handler.list_authors, methods=["GET"])
    router.add_api_route("/{author_id}/", handler.retrieve_author, methods=["GET"])
    router.add_api_route("/", handler.create_author, methods=["POST"], status_code=201)
    router.add_api_route("/{author_id}/", handler.delete_author, methods=["DELETE"])
    return router
