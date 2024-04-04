from unittest import mock
from ..stubs.book_stubs import books_stub

repository = mock.Mock()


def initialize():
    repository.list.return_value = books_stub
    repository.find_one.return_value = books_stub[0]
    repository.create.return_value = books_stub[0]
    repository.delete.return_value = True
