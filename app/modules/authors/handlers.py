from . import schemas
from fastapi import HTTPException, Response
from app.modules.authors.crud import AuthorRepository


class AuthorHandler:
    def __init__(self, repository: AuthorRepository):
        self.repository = repository

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
