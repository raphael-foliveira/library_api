from fastapi.testclient import TestClient

from app.main import app
from app.modules.authors.repository import AuthorRepository
from app.modules.authors.routes import get_author_repository
from tests.database.db import sessionmaker_test, engine_test
from app.database.config import Base
from app.modules.authors.models import *
from app.modules.books.models import *
from tests.factories import fake_author_create, fake_author_model

client = TestClient(app)


def override_get_author_repository():
    return AuthorRepository(sessionmaker_test)


class TestAuthorsRoutes:
    @classmethod
    def setup_class(cls):
        app.dependency_overrides[get_author_repository] = override_get_author_repository
        cls.repository = AuthorRepository(sessionmaker_test)
        Base.metadata.create_all(engine_test)

    def setup_method(self):
        with sessionmaker_test() as session:
            author1 = fake_author_model()
            author2 = fake_author_model()

            session.add(author1)
            session.add(author2)
            session.commit()

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

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(engine_test)
