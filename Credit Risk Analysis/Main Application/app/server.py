from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

cache = Cache()
db = SQLAlchemy()


def create_database(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
