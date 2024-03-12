from unittest import mock
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.modules.authors.repository import AuthorRepository
from app.modules.authors.routes import get_author_repository
from ..stubs.author_stubs import authors_entities_stub, authors_schemas_stub

client = TestClient(app)


author_repository_mock: AuthorRepository = mock.Mock()


@pytest.fixture
def setup():
    author_repository_mock.list.return_value = authors_entities_stub
    author_repository_mock.find.return_value = authors_entities_stub[0]
    author_repository_mock.create.return_value = authors_entities_stub[0]
    author_repository_mock.delete.return_value = True


def override_get_author_repository():
    return author_repository_mock


def setup_module():
    app.dependency_overrides[get_author_repository] = override_get_author_repository


def test_get_all_authors(setup):
    response = client.get("/authors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == len(authors_entities_stub)


def test_find_author(setup):
    response = client.get(f"/authors/")
    assert response.status_code == 200


def test_find_non_existing_author(setup):
    non_existing_author_id = 650
    author_repository_mock.find.return_value = None
    response = client.get(f"/authors/{non_existing_author_id}")
    assert response.status_code == 404


def test_create_author(setup):
    response = client.post("/authors", json={"first_name": "John", "last_name": "Doe"})
    assert response.status_code == 201


def test_create_invalid_author(setup):
    response = client.post("/authors", json={"foo": "John", "bar": "Doe"})
    assert response.status_code == 422


def test_delete_author(setup):
    response = client.delete(f"/authors/{authors_entities_stub[0].id}")
    assert response.status_code == 204


def test_delete_non_existing_author(setup):
    non_existing_author_id = 650
    author_repository_mock.delete.return_value = False
    response = client.delete(f"/authors/{non_existing_author_id}")
    author_repository_mock.delete.return_value = True
    assert response.status_code == 404
