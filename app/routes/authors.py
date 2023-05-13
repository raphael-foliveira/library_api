from fastapi import APIRouter, HTTPException, Response

from app import schemas
from app.crud.authors import AuthorRepository


class AuthorRouter:
    def __init__(self, repository: AuthorRepository):
        self.repository = repository
        self.router = APIRouter(
            prefix="/authors",
            tags=["authors"],
        )
        self.__add_routes()

    def __add_routes(self):
        self.router.add_api_route("/", self.list_authors, methods=["GET"])
        self.router.add_api_route(
            "/{author_id}/", self.retrieve_author, methods=["GET"]
        )
        self.router.add_api_route(
            "/", self.create_author, methods=["POST"], status_code=201
        )
        self.router.add_api_route(
            "/{author_id}/", self.delete_author, methods=["DELETE"]
        )

    async def list_authors(self) -> list[schemas.Author]:
        return self.repository.list()

    async def retrieve_author(
        self,
        author_id: int,
    ) -> schemas.Author:
        try:
            return self.repository.find(author_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=e.args[0])

    async def create_author(
        self,
        author: schemas.AuthorCreate,
    ) -> schemas.Author:
        try:
            return self.repository.create(author)
        except Exception as e:
            raise HTTPException(status_code=400, detail=e.args[0])

    async def delete_author(
        self,
        author_id: int,
    ) -> Response:
        if self.repository.delete(author_id):
            return Response(status_code=204)
        raise HTTPException(status_code=404, detail="Author not found")
