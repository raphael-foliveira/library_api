
from typing import List
from fastapi import APIRouter
import models

import schemas
from crud import AuthorRepository

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.get("/")
async def list_authors(limit: int = 100) -> list[schemas.Author]:
    return AuthorRepository().list(limit)  # type:ignore


@router.get("/{author_id}")
async def retrieve_author(author_id: int) -> schemas.Author:
    return AuthorRepository().find(author_id)


@router.post("/")
async def create_author(author: schemas.AuthorCreate) -> schemas.Author:
    return AuthorRepository().create(author)


@router.delete("/{author_id}")
async def delete_author(author_id: int) -> schemas.Author:
    return AuthorRepository().delete(author_id)
