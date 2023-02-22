
from database import Session


def db_session(func):
    def wrapper(*args, **kwargs):
        with Session() as db:
            kwargs['db'] = db
            return func(*args, **kwargs)
    return wrapper
