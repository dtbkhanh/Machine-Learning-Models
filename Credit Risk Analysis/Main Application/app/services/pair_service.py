import pandas as pd
import random


class PairService:

    def __init__(self, db, model):
        self.db = db
        self.model = model

    def load_pairs(self):
        # LOAD DB
        ActionCapture, PairList, User = self.model
        admin = User(user_mail='gerardocorado@creditshelf.com', user_name='Gerardo')
        self.db.session.add(admin)
        self.db.session.commit()

    def get_user_list(self):
        ActionCapture, PairList, User = self.model
        return User.query.all()


    def get_compare_companies(self):
        # -----------------------------------------------------------------------------------#
        # ----------------------------------- Dataframe -------------------------------------#

        # Read csv file into dataframe:
        # df = pd.read_csv('./Sample data.csv', sep = ';')
        df = pd.read_sql_table("Joined_Dataset_final", con=self.engine)

        # Group by Company IDs:
        group = df.groupby(['company_id_1', 'company_id_2']).size().reset_index()

        # Split the dataframe into two comparing pairs:
        pairID = list(range(1, 1000))
        random.shuffle(pairID)
        pairIndex = 0
        # print(pairID[0])
        temp_df = df.loc[df['pair_id'] == pairID[pairIndex]]

        df1 = temp_df.iloc[:, 0:8]
        df1 = df1.rename(columns={"company_name_1": "Company Name",
                                  "year_1": "Year",
                                  "revenue_1": "Revenues",
                                  "depreciation_amortization_1": "Depreciation and Amortization",
                                  "operating_profit_1": "Operating Profits",
                                  "interest_expense_1": "Interest Expense"})
        df2 = temp_df.iloc[:, 8:]
        df2 = df2.rename(columns={"company_name_2": "Company Name",
                                  "year_2": "Year",
                                  "revenue_2": "Revenues",
                                  "depreciation_amortization_2": "Depreciation and Amortization",
                                  "operating_profit_2": "Operating Profits",
                                  "interest_expense_2": "Interest Expense"})
        return df1, df2
