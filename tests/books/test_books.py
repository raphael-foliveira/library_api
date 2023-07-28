import io
from typing import Mapping
from fastapi import Depends
from fastapi.testclient import TestClient

from app.main import app
from app.modules.authors.routes import get_author_repository
from app.modules.books.repository import BookRepository
from app.modules.books.routes import get_books_repository, get_upload_path
from tests.authors.test_authors import override_get_author_repository
from tests.database.db import get_test_db, sessionmaker_test, engine_test
from app.modules.authors.models import *
from app.modules.books.models import *
from tests.factories import (
    fake_author_model,
    fake_book_model,
    fake_book_schema,
)
from sqlalchemy.orm.session import Session

client = TestClient(app)


def override_get_books_repository(db: Session = Depends(get_test_db)):
    return BookRepository(db)


class TestBooksRoutes:
    @classmethod
    def setup_class(cls):
        app.dependency_overrides[get_author_repository] = override_get_author_repository
        app.dependency_overrides[get_books_repository] = override_get_books_repository

    def setup_method(self):
        print("setting up")
        Base.metadata.create_all(engine_test)
        with sessionmaker_test() as session:
            for _ in range(15):
                author = fake_author_model()
                session.add(author)
                session.commit()
                book = fake_book_model()
                book.author_id = author.id  # type: ignore
                session.add(book)
            session.commit()

    def teardown_method(self):
        print("tearing down")
        Base.metadata.drop_all(engine_test)

    def test_get_all_books(self):
        response = client.get("/books/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_find_book(self):
        response = client.get(f"/books/1")
        assert response.status_code == 200

    def test_find_non_existing_book(self):
        response = client.get(f"/books/650")
        assert response.status_code == 404

    def test_create_book(self):
        mock_book = fake_book_schema()
        mock_book.author_id = 1  # type: ignore
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

    def test_delete_book(self):
        response = client.delete(f"/books/2")
        assert response.status_code == 204

    def test_delete_non_existing_book(self):
        response = client.delete(f"/books/650")
        assert response.status_code == 404

    def test_get_upload_path(self):
        upload_path = get_upload_path("1")
        assert upload_path == "./uploads/1"

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(engine_test)
