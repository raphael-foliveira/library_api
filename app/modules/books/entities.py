from dataclasses import dataclass
from datetime import datetime


@dataclass
class Book:
    id: int
    title: str
    release_date: datetime
    number_of_pages: int
    author_id: int
    image_url: str
