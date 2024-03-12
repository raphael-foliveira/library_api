from typing import Optional
from faker import Faker
from app.modules.authors.entities import Author
from app.modules.books.entities import Book
from app.modules.authors.models import AuthorModel
from app.modules.books.models import BookModel
from app.modules.authors import schemas
from datetime import date

fake = Faker()


def fake_author_entity():
    return Author(id=fake.random_int(), first_name=fake.name(), last_name=fake.name())


def fake_book_entity(author_id: Optional[int] = None):
    return Book(
        id=fake.random_int(),
        title=fake.name(),
        author_id=author_id or fake.random_int(min=1, max=9999),
        release_date=date.today(),
        number_of_pages=fake.random_int(min=100, max=1000),
        image_url=fake.url(),
    )


def fake_author_model(include_id: bool = False):
    if include_id:
        return AuthorModel(
            id=fake.random_int(), first_name=fake.name(), last_name=fake.name()
        )
    return AuthorModel(first_name=fake.name(), last_name=fake.name())


def fake_book_model(include_id: bool = False):
    if include_id:
        return BookModel(
            id=fake.random_int(),
            title=fake.name(),
            author_id=fake.random_int(min=1, max=9999),
            release_date=date.today(),
            number_of_pages=fake.random_int(min=100, max=1000),
            image_url=fake.url(),
        )
    return BookModel(
        title=fake.name(),
        author_id=fake.random_int(min=1, max=9999),
        release_date=date.today(),
        number_of_pages=fake.random_int(min=100, max=1000),
        image_url=fake.url(),
    )


def fake_author_schema():
    return schemas.Author(
        id=fake.random_int(), first_name=fake.name(), last_name=fake.name()
    )


def fake_book_schema():
    return schemas.Book(
        id=fake.random_int(),
        title=fake.name(),
        author_id=fake.random_int(),
        release_date=fake.date(),
        number_of_pages=fake.random_int(),
        image_url=fake.url(),
    )


def fake_author_create():
    return schemas.AuthorCreate(first_name=fake.name(), last_name=fake.name())


def fake_book_create():
    return BookModel(
        title=fake.name(),
        author_id=fake.random_int(min=1, max=9999),
        release_date=f"{fake.random_int(min=1900, max=2023)}-{fake.random_int(min=1, max=12)}-{fake.random_int(min=1, max=28)}",
        number_of_pages=fake.random_int(min=100, max=1000),
        image_url=fake.url(),
    )


def fake_book_create_dict():
    return {
        "id": fake.random_int(),
        "title": fake.name(),
        "author_id": fake.random_int(min=1, max=9999),
        "release_date": f"{fake.random_int(min=1900, max=2023)}-{fake.random_int(min=1, max=12)}-{fake.random_int(min=1, max=28)}",
        "number_of_pages": fake.random_int(min=100, max=1000),
        "image_url": fake.url(),
    }
