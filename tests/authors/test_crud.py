# type:ignore

import pytest
from app.authors.crud import AuthorRepository
from app.authors.models import Author
from app.schemas.authors import AuthorCreate
from tests.database.mock_config import mock_engine, mock_session
from tests.factories import fake_author_model


class TestAuthorsRepository:
    def setup_method(self):
        self.repository = AuthorRepository(mock_engine)
        with mock_session() as session:
            session.add(fake_author_model())
            session.add(fake_author_model())
            session.commit()

    def test_list(self):
        assert len(self.repository.list()) > 0

    def test_create(self):
        initial_length = len(self.repository.list())
        author_data: AuthorCreate = fake_author_model()
        new_author = self.repository.create(author_data)
        assert new_author.first_name == author_data.first_name
        assert len(self.repository.list()) > initial_length
        assert new_author in self.repository.list()

    def test_delete(self):
        initial_length = len(self.repository.list())
        author_to_delete = self.repository.list()[0]
        self.repository.delete(author_to_delete.id)
        assert len(self.repository.list()) < initial_length
        assert author_to_delete not in self.repository.list()

    def test_find(self):
        first_author = self.repository.list()[0]
        found_author = self.repository.find(first_author.id)
        assert found_author.id == first_author.id
        with pytest.raises(Exception):
            self.repository.find(650)

    def teardown_method(self):
        with mock_session() as session:
            session.query(Author).delete()
            session.commit()
