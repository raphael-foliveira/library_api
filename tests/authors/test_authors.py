from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from app.database.config import Base
from app.main import app
from app.modules.authors.models import Author
from app.modules.authors.repository import AuthorRepository
from app.modules.authors.routes import get_author_repository
from tests.database.db import engine_test, get_test_db, sessionmaker_test
from tests.factories import fake_author_model

client = TestClient(app)


def override_get_author_repository(db: Session = Depends(get_test_db)):
    return AuthorRepository(db)


class TestAuthorsRoutes:
    @classmethod
    def setup_class(cls):
        app.dependency_overrides[get_author_repository] = override_get_author_repository
        cls.repository = override_get_author_repository()
        print("creating tables")
        Base.metadata.create_all(engine_test)
        cls.author_ids = []

    @classmethod
    def teardown_class(cls):
        print("deleting tables")
        Base.metadata.drop_all(engine_test)

    def setup_method(self):
        print("setting up")
        with sessionmaker_test() as session:
            authors = [fake_author_model() for _ in range(5)]
            session.add_all(authors)
            session.commit()
            self.author_ids = [author.id for author in session.query(Author).all()]

    def teardown_method(self):
        print("tearing down")
        with sessionmaker_test() as session:
            for author in session.query(Author).all():
                session.delete(author)
            session.commit()

    def test_get_all_authors(self):
        response = client.get("/authors")
        assert response.status_code == 200

    def test_find_author(self):
        for author_id in self.author_ids:
            response = client.get(f"/authors/{author_id}")
            assert response.status_code == 200

    def test_find_non_existing_author(self):
        non_existing_author_id = 650
        while non_existing_author_id in self.author_ids:
            non_existing_author_id += 1
        response = client.get(f"/authors/{non_existing_author_id}")
        assert response.status_code == 404

    def test_create_author(self):
        response = client.post(
            "/authors", json={"first_name": "John", "last_name": "Doe"}
        )
        assert response.status_code == 201

    def test_create_invalid_author(self):
        response = client.post("/authors", json={"foo": "John", "bar": "Doe"})
        assert response.status_code == 422

    def test_delete_author(self):
        for author_id in self.author_ids:
            response = client.delete(f"/authors/{author_id}")
            assert response.status_code == 204

    def test_delete_non_existing_author(self):
        non_existing_author_id = 650
        while non_existing_author_id in self.author_ids:
            non_existing_author_id += 1
        response = client.get(f"/authors/{non_existing_author_id}")
        assert response.status_code == 404
