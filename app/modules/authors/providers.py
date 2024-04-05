from .repository import AuthorRepository
from ...database.config import session


def get_author_repository():
    return AuthorRepository(session=session)
