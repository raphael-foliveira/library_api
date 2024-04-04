import io
from typing import Mapping
from fastapi.testclient import TestClient

from app.app import app
from app.modules.authors.routes import get_author_repository
from app.modules.books.providers import get_upload_path
from app.modules.books.routes import get_books_repository
from tests.authors.test_authors import override_get_author_repository
from tests.factories import (
    fake_book_schema,
)
from typing import Any
from ..stubs.book_stubs import books_stub
from ..mocks import book_mocks

client = TestClient(app)


def override_get_books_repository():
    return book_mocks.repository


def setup_module():
    app.dependency_overrides[get_author_repository] = override_get_author_repository
    app.dependency_overrides[get_books_repository] = override_get_books_repository


def setup_function():
    book_mocks.initialize()


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
    book_mocks.repository.find_one.return_value = None
    response = client.get(f"/books/{non_existing_book_id}")
    assert response.status_code == 404


def test_create_book():
    fake_book = fake_book_schema()
    fake_book.author_id = 1
    response = client.post(
        "/books/",
        json={
            "title": fake_book.title,
            "author_id": fake_book.author_id,
            "release_date": fake_book.release_date.strftime("%Y-%m-%d"),
            "number_of_pages": fake_book.number_of_pages,
            "image_url": fake_book.image_url,
        },
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
    book_mocks.repository.delete.return_value = False
    response = client.delete(f"/books/{non_existing_book_id}")
    assert response.status_code == 404
    book_mocks.repository.delete.return_value = True


def test_get_upload_path():
    upload_path = get_upload_path("1")
    assert upload_path == "./uploads/1"
