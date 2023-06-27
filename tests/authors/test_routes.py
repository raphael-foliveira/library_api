from fastapi.testclient import TestClient

from app.main import app
from app.modules.authors.crud import AuthorRepository
from tests.database.mock_config import mock_session
from tests.factories import fake_author_create

client = TestClient(app)


class TestAuthorsRoutes:
    def setup_method(self):
        self.repository = AuthorRepository(mock_session)

    def test_get_all_authors(self):
        response = client.get("/authors")
        assert response.status_code == 200

    def test_find_author(self):
        mock_author = fake_author_create()
        created_author = self.repository.create(mock_author)
        response = client.get(f"/authors/{created_author.id}")
        assert response.status_code == 200

    def test_create_author(self):
        response = client.post(
            "/authors", json={"first_name": "John", "last_name": "Doe"}
        )
        assert response.status_code == 201

    def test_create_invalid_author(self):
        response = client.post("/authors", json={"foo": "John", "bar": "Doe"})
        print(response.json())
        assert response.status_code == 422

    def test_delete_author(self):
        mock_author = fake_author_create()
        created_author = self.repository.create(mock_author)
        print(created_author.id)
        response = client.delete(f"/authors/{created_author.id}")
        assert response.status_code == 204

    def test_delete_non_existing_author(self):
        response = client.get(f"/authors/650")
        assert response.status_code == 404
