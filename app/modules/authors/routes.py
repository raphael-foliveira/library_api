from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm.session import Session

from app.database.config import get_db
from app.modules.authors.repository import AuthorRepository
from app.modules.authors.schemas import AuthorCreate

authors_router = APIRouter(prefix="/authors", tags=["authors"])


def get_author_repository(db: Session = Depends(get_db)):
    return AuthorRepository(db)


@authors_router.get("/")
def list_authors(repository: AuthorRepository = Depends(get_author_repository)):
    return repository.list()


@authors_router.get("/{author_id}/")
def retrieve_author(
    author_id: int, repository: AuthorRepository = Depends(get_author_repository)
):
    return repository.find(author_id)


@authors_router.post("/", status_code=201)
def create_author(
    author: AuthorCreate, repository: AuthorRepository = Depends(get_author_repository)
):
    return repository.create(author)


@authors_router.delete("/{author_id}/")
def delete_author(
    author_id: int, repository: AuthorRepository = Depends(get_author_repository)
):
    repository.delete(author_id)
    return Response(status_code=204)
