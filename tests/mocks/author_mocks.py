from unittest import mock
from ..stubs.author_stubs import authors_entities_stub


repository = mock.Mock()


def initialize():
    repository.list.return_value = authors_entities_stub
    repository.find_one.return_value = authors_entities_stub[0]
    repository.create.return_value = authors_entities_stub[0]
    repository.delete.return_value = True
