from fastapi import APIRouter, Depends, HTTPException
from app.modules.authors.repository import AuthorRepository
from .schemas import Author, AuthorCreate
from .providers import get_author_repository

authors_router = APIRouter(prefix="/authors", tags=["authors"])


@authors_router.get("/", response_model=list[Author])
def list_authors(
    repository: AuthorRepository = Depends(get_author_repository),
):
    result = repository.list()
    return result


@authors_router.get("/{author_id}/", response_model=Author)
def retrieve_author(
    author_id: int, repository: AuthorRepository = Depends(get_author_repository)
):
    author = repository.find_one(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@authors_router.post("/", status_code=201, response_model=Author)
def create_author(
    author: AuthorCreate,
    repository: AuthorRepository = Depends(get_author_repository),
):
    return repository.create(author)


@authors_router.delete("/{author_id}/", status_code=204)
def delete_author(
    author_id: int, repository: AuthorRepository = Depends(get_author_repository)
) -> None:
    ok = repository.delete(author_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Author not found")
