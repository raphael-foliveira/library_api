from fastapi import APIRouter, HTTPException, Response

from app import schemas
from app.crud.authors import AuthorRepository

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.get("/")
async def list_authors() -> list[schemas.Author]:
    return AuthorRepository().list()


@router.get("/{author_id}")
async def retrieve_author(author_id: int) -> schemas.Author:
    return AuthorRepository().find(author_id)


@router.post("/")
async def create_author(author: schemas.AuthorCreate) -> schemas.Author:
    return AuthorRepository().create(author)


@router.delete("/{author_id}")
async def delete_author(author_id: int) -> Response:
    if AuthorRepository().delete(author_id):
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Author not found")
