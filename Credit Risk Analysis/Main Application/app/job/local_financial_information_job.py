import pandas as pd
from stories import story, arguments, Success, Failure, Result


class LoadFinancialInformationJob:

    def __init__(self, engine):
        self.engine = engine

    @story
    @arguments('file_path')
    def load_data(I):
        I.load_file
        # I.save_in_db

    def load_file(self, ctx):
        ctx.df = pd.read_csv(ctx.file_path, sep=';')
        return Success()

    def save_in_db(self, ctx):
        return Success()
