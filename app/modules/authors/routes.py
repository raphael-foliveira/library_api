from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from app.database.config import get_db
from app.modules.authors.repository import AuthorRepository
from . import schemas

authors_router = APIRouter(prefix="/authors", tags=["authors"])


def get_author_repository(db: Session = Depends(get_db)):
    return AuthorRepository(db)


@authors_router.get("/", response_model=list[schemas.Author])
def list_authors(
    repository: AuthorRepository = Depends(get_author_repository),
):
    result = repository.list()
    return result


@authors_router.get("/{author_id}/", response_model=schemas.Author)
def retrieve_author(
    author_id: int, repository: AuthorRepository = Depends(get_author_repository)
):
    author = repository.find(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@authors_router.post("/", status_code=201, response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
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
