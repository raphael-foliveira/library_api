import pytest
from tests.database.mock_config import mock_engine, mock_session
from app.models.books import Book
from app.crud.books import BookRepository
from unittest.mock import Mock
from datetime import date
from faker import Faker

fake = Faker()


def fake_book():
    return Book(
        title=fake.name(),
        author_id=fake.random_int(min=1, max=100),
        release_date=date.today(),
        number_of_pages=fake.random_int(min=100, max=1000),
        image_url=fake.url(),
    )


class TestBooksRepository:
    def setup_method(self):
        self.repository = BookRepository(mock_engine)
        with mock_session() as session:
            session.add(fake_book())
            session.add(fake_book())
            session.commit()

    def test_list(self):
        assert len(self.repository.list()) > 0

    def test_create(self):
        initial_length = len(self.repository.list())
        book_mock = fake_book()
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
