from sqlalchemy import func, create_engine
from os import environ
from app.utils import get_db_url


class DB:
    def __init__(self, engine_db, url_db):
        self.engine_db = engine_db
        self.url = url_db


def init_db() -> DB:
    url = get_db_url()
    # engine_db = setup_db(url)
    return DB(None, url)


def setup_db(url):
    return create_engine(url)



