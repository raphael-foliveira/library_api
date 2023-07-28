import io
from typing import Generator, Mapping
from fastapi import Depends
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.modules.authors.routes import get_author_repository
from app.modules.books.repository import BookRepository
from app.modules.books.routes import get_books_repository, get_upload_path
from tests.authors.test_authors import override_get_author_repository
from tests.database.db import get_test_db, sessionmaker_test, engine_test
from app.modules.books.models import Book
from app.database.config import Base
from tests.factories import (
    fake_author_model,
    fake_book_model,
    fake_book_schema,
)
from sqlalchemy.orm.session import Session
from typing import Any

client = TestClient(app)


def override_get_books_repository(db: Session = Depends(get_test_db)):
    return BookRepository(db)


@pytest.fixture
def database_book_ids() -> Generator[list[int], None, None]:
    with sessionmaker_test() as session:
        for _ in range(5):
            author = fake_author_model()
            session.add(author)
            session.commit()
            book = fake_book_model()
            book.author_id = author.id
            session.commit()
        yield [book.id for book in session.query(Book).all()]
        for book in session.query(Book).all():
            session.delete(book)
        session.commit()


class TestBooksRoutes:
    @classmethod
    def setup_class(cls):
        app.dependency_overrides[get_author_repository] = override_get_author_repository
        app.dependency_overrides[get_books_repository] = override_get_books_repository
        Base.metadata.create_all(engine_test)

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(engine_test)

    def test_get_all_books(self, database_book_ids):
        response = client.get("/books/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == len(database_book_ids)

    def test_find_book(self, database_book_ids):
        for book_id in database_book_ids:
            response = client.get(f"/books/{book_id}")
            assert response.status_code == 200

    def test_find_non_existing_book(self, database_book_ids):
        non_existing_book_id = 650
        while non_existing_book_id in database_book_ids:
            non_existing_book_id += 1
        response = client.get(f"/books/{non_existing_book_id}")
        assert response.status_code == 404

    def test_create_book(self):
        mock_book = fake_book_schema()
        mock_book.author_id = 1
        form_data: Mapping[str, Any] = {
            "title": mock_book.title,
            "release_date": mock_book.release_date.strftime("%Y-%m-%d"),
            "number_of_pages": str(mock_book.number_of_pages),
            "author_id": mock_book.author_id,
        }
        file_data = io.BytesIO(b"test_image_content")
        response = client.post(
            "/books/",
            data=form_data,
            files={"image": ("test_image.jpg", file_data, "image/jpeg")},
        )
        assert response.status_code == 201

    def test_create_invalid_book(self):
        form_data: Mapping[str, Any] = {"foo": "bar", "spam": "eggs"}
        response = client.post(
            "/books/",
            data=form_data,
        )
        assert response.status_code == 422

    def test_delete_book(self, database_book_ids):
        for book_id in database_book_ids:
            response = client.delete(f"/books/{book_id}")
            assert response.status_code == 204

    def test_delete_non_existing_book(self, database_book_ids):
        non_existing_book_id = 650
        while non_existing_book_id in database_book_ids:
            non_existing_book_id += 1
        response = client.delete(f"/books/{non_existing_book_id}")
        assert response.status_code == 404

    def test_get_upload_path(self):
        upload_path = get_upload_path("1")
        assert upload_path == "./uploads/1"
