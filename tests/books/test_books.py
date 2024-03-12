import io
from typing import Mapping
from unittest import mock
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.modules.authors.routes import get_author_repository
from app.modules.books.routes import get_books_repository, get_upload_path
from tests.authors.test_authors import override_get_author_repository
from tests.factories import (
    fake_book_schema,
)
from typing import Any
from ..stubs.book_stubs import books_stub

client = TestClient(app)

book_repository_mock = mock.Mock()


def override_get_books_repository():
    return book_repository_mock


def setup_function():
    book_repository_mock.list.return_value = books_stub
    book_repository_mock.find.return_value = books_stub[0]
    book_repository_mock.create.return_value = books_stub[0]
    book_repository_mock.delete.return_value = True
    app.dependency_overrides[get_author_repository] = override_get_author_repository
    app.dependency_overrides[get_books_repository] = override_get_books_repository


def test_get_all_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == len(books_stub)


def test_find_book():
    response = client.get(f"/books/{books_stub[0].id}")
    assert response.status_code == 200


def test_find_non_existing_book():
    non_existing_book_id = 650
    book_repository_mock.find.return_value = None
    response = client.get(f"/books/{non_existing_book_id}")
    assert response.status_code == 404


def test_create_book():
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


def test_create_invalid_book():
    form_data: Mapping[str, Any] = {"foo": "bar", "spam": "eggs"}
    response = client.post(
        "/books/",
        data=form_data,
    )
    assert response.status_code == 422


def test_delete_book():
    response = client.delete(f"/books/{books_stub[0].id}")
    assert response.status_code == 204


def test_delete_non_existing_book():
    non_existing_book_id = 650
    book_repository_mock.delete.return_value = False
    response = client.delete(f"/books/{non_existing_book_id}")
    assert response.status_code == 404
    book_repository_mock.delete.return_value = True


def test_get_upload_path():
    upload_path = get_upload_path("1")
    assert upload_path == "./uploads/1"
