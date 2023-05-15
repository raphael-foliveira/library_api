# type: ignore

import pytest

from app.books.crud import BookRepository
from app.books.models import Book
from tests.database.mock_config import mock_engine, mock_session
from tests.factories import fake_book_model


class TestBooksRepository:
    def setup_method(self):
        self.repository = BookRepository(mock_engine)
        with mock_session() as session:
            session.add(fake_book_model())
            session.add(fake_book_model())
            session.commit()

    def test_list(self):
        assert len(self.repository.list()) > 0

    def test_create(self):
        initial_length = len(self.repository.list())
        book_mock = fake_book_model()
        new_book = self.repository.create(book_mock)
        assert new_book in self.repository.list()
        assert new_book.title == book_mock.title
        assert len(self.repository.list()) > initial_length

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
        with mock_session() as session:
            session.query(Book).delete()
            session.commit()
