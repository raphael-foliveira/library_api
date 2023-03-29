from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from app.main import app
from unittest.mock import patch
from tests.factories import fake_author_schema


client = TestClient(app)


class TestAuthorsRoutes:
    @patch("app.crud.authors.AuthorRepository.list")
    def test_get_all_authors(self, mock_repository):
        author = fake_author_schema()
        mock_repository.return_value = [author]
        response = client.get("/authors")
        assert response.status_code == 200
        assert response.json() == [author]

    @patch("app.crud.authors.AuthorRepository.find")
    def test_find_author(self, mock_repository):
        author = fake_author_schema()
        mock_repository.return_value = author
        response = client.get("/authors/1")
        assert response.status_code == 200
        assert response.json() == author
        mock_repository.side_effect = HTTPException(404, "Not Found")
        response = client.get(f"/authors/650")
        assert response.status_code == 404

    @patch("app.crud.authors.AuthorRepository.create")
    def test_create_author(self, mock_repository):
        mock_author = fake_author_schema()
        mock_repository.return_value = mock_author
        response = client.post(
            "/authors", json={"first_name": "John", "last_name": "Doe"}
        )
        assert response.status_code == 201
        assert response.json() == mock_author
        mock_repository.side_effect = HTTPException(400, "Bad Request")
        response = client.post(
            "/authors", json={"first_name": "John", "last_name": "Doe"}
        )
        assert response.status_code == 400

    @patch("app.crud.authors.AuthorRepository.delete")
    def teste_delete_author(self, mock_repository):
        mock_repository.return_value = True
        response = client.delete("/authors/1")
        assert response.status_code == 204
        mock_repository.return_value = False
        response = client.get(f"/authors/650")
        assert response.status_code == 404
