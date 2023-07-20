import pytest
from app.modules.authors.crud import AuthorRepository
from app.modules.books.crud import BookRepository

from app.modules.books.models import Book
from tests.database.db import sessionmaker_test, engine_test
from app.database.config import Base
from tests.factories import fake_author_model, fake_book_model


class TestBooksRepository:
    @classmethod
    def setup_class(cls):
        cls.author_repository = AuthorRepository(sessionmaker_test)
        cls.repository = BookRepository(sessionmaker_test)
        Base.metadata.create_all(engine_test)

    def setup_method(self):
        with sessionmaker_test() as session:
            author1 = fake_author_model()
            author2 = fake_author_model()

            book1 = fake_book_model()
            book1.author_id = author1.id  # type: ignore

            book2 = fake_book_model()
            book2.author_id = author2.id  # type: ignore

            session.add(author1)
            session.add(author2)
            session.add(book1)
            session.add(book2)
            session.commit()

    def test_list(self):
        assert len(self.repository.list()) > 0

    def test_create(self):
        author_mock = self.author_repository.list()[0]
        book_mock = fake_book_model()
        book_mock.author_id = author_mock.id  # type: ignore
        new_book = self.repository.create(book_mock)
        assert new_book in self.repository.list()
        assert new_book.title == book_mock.title

    def test_delete(self):
        initial_length = len(self.repository.list())
        book_to_delete = self.repository.list()[0]
        self.repository.delete(book_to_delete.id)
        assert len(self.repository.list()) < initial_length
        assert book_to_delete not in self.repository.list()

    def test_find(self):
        first_book = self.repository.list()[0]
        found_book = self.repository.find(first_book.id)
        assert found_book.id == first_book.id
        with pytest.raises(Exception):
            self.repository.find(650)

    def teardown_method(self):
        with sessionmaker_test() as session:
            session.query(Book).delete()
            session.commit()

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(engine_test)
