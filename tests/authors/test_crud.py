import pytest
from app.modules.authors.crud import AuthorRepository
from app.modules.authors.models import Author
from app.modules.authors.schemas import AuthorCreate
from tests.database.mock_config import mock_sessionmaker, mock_engine
from app.database.config import Base
from tests.factories import fake_author_model


class TestAuthorsRepository:
    @classmethod
    def setup_class(cls):
        cls.repository = AuthorRepository(mock_sessionmaker)
        Base.metadata.create_all(mock_engine)

    def setup_method(self):
        with mock_sessionmaker() as session:
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
        with mock_sessionmaker() as session:
            session.query(Author).delete()
            session.commit()

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(mock_engine)
