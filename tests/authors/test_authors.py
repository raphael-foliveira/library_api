from fastapi.testclient import TestClient
from app.app import app
from app.modules.authors.routes import get_author_repository
from ..stubs.author_stubs import authors_entities_stub
from ..mocks import author_mocks

client = TestClient(app)


def setup_function():
    author_mocks.initialize()


def override_get_author_repository():
    return author_mocks.repository


def setup_module():
    app.dependency_overrides[get_author_repository] = override_get_author_repository


def test_get_all_authors():
    response = client.get("/authors")
    body = response.json()
    assert response.status_code == 200
    assert isinstance(body, list)
    assert len(body) == len(authors_entities_stub)


def test_find_author():
    response = client.get(f"/authors/")
    assert response.status_code == 200


def test_find_non_existing_author():
    non_existing_author_id = 650
    author_mocks.repository.find_one.return_value = None
    response = client.get(f"/authors/{non_existing_author_id}")
    assert response.status_code == 404


def test_create_author():
    response = client.post("/authors", json={"first_name": "John", "last_name": "Doe"})
    assert response.status_code == 201


def test_create_invalid_author():
    response = client.post("/authors", json={"foo": "John", "bar": "Doe"})
    assert response.status_code == 422


def test_delete_author():
    response = client.delete(f"/authors/{authors_entities_stub[0].id}")
    assert response.status_code == 204


def test_delete_non_existing_author():
    non_existing_author_id = 650
    author_mocks.repository.delete.return_value = False
    response = client.delete(f"/authors/{non_existing_author_id}")
    author_mocks.repository.delete.return_value = True
    assert response.status_code == 404
