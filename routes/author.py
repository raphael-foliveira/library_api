
from typing import List
from fastapi import APIRouter

import schemas
from crud import AuthorRepository

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.get("/")
def list_authors(limit: int = 100, author_name: str = "") -> list[schemas.Author]:
    if author_name != "":
        return AuthorRepository().find_by_name(author_name)  # type: ignore
    return AuthorRepository().list(limit)  # type: ignore


@router.get("/{author_id}")
def retrieve_author(author_id: int) -> schemas.Author:
    return AuthorRepository().find(author_id)


@router.post("/")
def create_author(author: schemas.AuthorCreate) -> schemas.Author:
    return AuthorRepository().create(author)


@router.delete("/{author_id}")
def delete_author(author_id: int) -> schemas.Author:
    return AuthorRepository().delete(author_id)
