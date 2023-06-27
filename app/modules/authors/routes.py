from fastapi import APIRouter, Depends, HTTPException, Response
from app.modules.authors.crud import AuthorRepository
from app.modules.authors.schemas import AuthorCreate
from app.database.config import session

authors_router = APIRouter(prefix="/authors", tags=["authors"])


def get_author_repository():
    return AuthorRepository(session)


@authors_router.get("/")
def list_authors(repository: AuthorRepository = Depends(get_author_repository)):
    return repository.list()


@authors_router.get("/{author_id}/")
def retrieve_author(
    author_id: int, repository: AuthorRepository = Depends(get_author_repository)
):
    try:
        return repository.find(author_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@authors_router.post("/", status_code=201)
def create_author(
    author: AuthorCreate, repository: AuthorRepository = Depends(get_author_repository)
):
    try:
        return repository.create(author)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@authors_router.delete("/{author_id}/")
def delete_author(
    author_id: int, repository: AuthorRepository = Depends(get_author_repository)
):
    if repository.delete(author_id):
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Author not found")
