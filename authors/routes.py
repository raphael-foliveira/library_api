from fastapi import APIRouter

from . import schemas
from .crud import AuthorRepository

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
async def delete_author(author_id: int) -> schemas.Author:
    return AuthorRepository().delete(author_id)
