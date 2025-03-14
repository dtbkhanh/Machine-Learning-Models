import fire

from app.server import db, cache
import app.services.models


class CLI(object):
    """A simple calculator class."""

    def db(self):
        print(f"use db")
        pass

    def etl(self, file=None):
        print(f"file_path:{file}")
        return file


if __name__ == '__main__':
    fire.Fire(CLI)
