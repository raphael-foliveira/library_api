from tests.factories import fake_book_entity
from .author_stubs import authors_entities_stub

books_stub = [fake_book_entity(author_id=author.id) for author in authors_entities_stub]
