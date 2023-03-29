from fastapi import APIRouter, HTTPException, Response, Depends

from app import schemas
from app.crud.authors import AuthorRepository, get_author_repository

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.get("/")
async def list_authors(
    repository: AuthorRepository = Depends(get_author_repository),
) -> list[schemas.Author]:
    return repository.list()


@router.get("/{author_id}/")
async def retrieve_author(
    author_id: int, repository: AuthorRepository = Depends(get_author_repository)
) -> schemas.Author:
    try:
        return repository.find(author_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@router.post("/", status_code=201)
async def create_author(
    author: schemas.AuthorCreate,
    repository: AuthorRepository = Depends(get_author_repository),
) -> schemas.Author:
    try:
        return repository.create(author)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@router.delete("/{author_id}/")
async def delete_author(
    author_id: int, repository: AuthorRepository = Depends(get_author_repository)
) -> Response:
    if repository.delete(author_id):
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Author not found")
