import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header, Request
import schemas
import models

from crud import AuthorRepository

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.get("/")
def list_authors(limit: int = 100, author_name: str = ""):
    if author_name != "":
        return AuthorRepository().find_by_name(author_name)
    return AuthorRepository().list(limit)


@router.get("/{author_id}")
def retrieve_author(author_id: int) -> models.Author:
    return AuthorRepository().find(author_id)


@router.post("/")
def create_author(author: schemas.AuthorCreate):
    return AuthorRepository().create(author)


@router.delete("/{author_id}")
def delete_author(author_id: int):
    return AuthorRepository().delete(author_id)
