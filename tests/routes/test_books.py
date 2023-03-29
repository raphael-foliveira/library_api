import io
from unittest.mock import patch
from fastapi import HTTPException

from app.routes.books import get_upload_path

from fastapi.testclient import TestClient

from app.main import app
from tests.factories import fake_author_schema, fake_book_schema
from tempfile import TemporaryDirectory

client = TestClient(app)


class TestBooksRoutes:
    @patch("app.crud.books.BookRepository.list")
    def test_get_all_books(self, mock_repository):
        mock_repository.return_value = [fake_book_schema()]
        response = client.get("/books/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @patch("app.crud.books.BookRepository.find")
    def test_find_book(self, mock_repository):
        mock_book = fake_book_schema()
        mock_repository.return_value = mock_book
        response = client.get(f"/books/{mock_book.id}")
        assert response.status_code == 200
        assert response.json().get("id") == mock_book.id
        mock_repository.side_effect = HTTPException(404, "Not Found")
        response = client.get(f"/books/650")
        assert response.status_code == 404

    @patch("app.routes.books.get_upload_path")
    @patch("app.crud.authors.AuthorRepository.find")
    @patch("app.crud.books.BookRepository.create")
    def test_create_book(
        self, mock_book_repository, mock_author_repository, mock_upload_path
    ):
        with TemporaryDirectory() as tmpdir:
            mock_upload_path.return_value = tmpdir

            book = fake_book_schema()
            mock_book_repository.return_value = book
            mock_author_repository.return_value = fake_author_schema()

            form_data = {
                "title": book.title,
                "release_date": book.release_date.strftime("%Y-%m-%d"),
                "number_of_pages": str(book.number_of_pages),
                "author_id": book.author_id,
            }
            file_data = io.BytesIO(b"test_image_content")
            response = client.post(
                "/books/",
                data=form_data,
                files={"image": ("test_image.jpg", file_data, "image/jpeg")},
            )
            assert response.status_code == 201
            mock_book_repository.side_effect = HTTPException(400, "Bad Request")
            response = client.post(
                "/books/",
                data=form_data,
                files={"image": ("test_image.jpg", file_data, "image/jpeg")},
            )
            assert response.status_code == 400

    @patch("app.crud.books.BookRepository.delete")
    def test_delete_book(
        self,
        mock_repository,
    ):
        mock_repository.return_value = True
        response = client.delete("/books/1")
        assert response.status_code == 204
        mock_repository.return_value = False
        response = client.get(f"/books/650")
        assert response.status_code == 404

    def test_get_upload_path(self):
        upload_path = get_upload_path(1)
        assert upload_path == "./uploads/1"
