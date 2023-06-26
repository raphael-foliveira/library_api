import io
from typing import Any, Mapping
from app.modules.authors.crud import AuthorRepository
from app.modules.books.crud import BookRepository

from app.modules.books.handlers import get_upload_path

from fastapi.testclient import TestClient

from app.main import app
from tests.database.mock_config import mock_session
from tests.factories import (
    fake_author_create,
    fake_book_create,
    fake_book_schema,
)

client = TestClient(app)


class TestBooksRoutes:
    def setup_method(self):
        self.book_repository = BookRepository(mock_session)
        self.author_repository = AuthorRepository(mock_session)

    def test_get_all_books(
        self,
    ):
        response = client.get("/books/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_find_book(self):
        mock_author_create = fake_author_create()
        mock_author = self.author_repository.create(mock_author_create)
        mock_book_create = fake_book_create()
        mock_book_create.author_id = mock_author.id  # type: ignore
        mock_book = self.book_repository.create(mock_book_create)

        print(mock_author)
        print(mock_book_create)
        response = client.get(f"/books/{mock_book.id}")
        assert response.status_code == 200

    def test_find_non_existing_book(self):
        response = client.get(f"/books/650")
        assert response.status_code == 404

    def test_create_book(self):
        mock_author_create = fake_author_create()
        mock_author = self.author_repository.create(mock_author_create)
        mock_book = fake_book_schema()
        mock_book.author_id = mock_author.id

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

    def test_delete_book(self):
        mock_author_create = fake_author_create()
        mock_author = self.author_repository.create(mock_author_create)
        mock_book_create = fake_book_create()
        mock_book_create.author_id = mock_author.id  # type: ignore
        mock_book = self.book_repository.create(mock_book_create)
        response = client.delete(f"/books/{mock_book.id}")
        assert response.status_code == 204

    def test_delete_non_existing_book(self):
        response = client.get(f"/books/650")
        assert response.status_code == 404

    def test_get_upload_path(self):
        upload_path = get_upload_path("1")
        assert upload_path == "./uploads/1"
