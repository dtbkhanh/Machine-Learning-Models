# -*- coding: utf-8 -*-

########################################################################
###### Group company pairs into different groups with an unique ID
###### Each group has exactly n pairs (now is 20)
########################################################################

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
from sqlalchemy import func, create_engine
import pandas as pd
import numpy as np
import random
import pymysql
import mysql.connector

### Connecting to a database:
engine = create_engine("mysql+pymysql://root:helloworld@localhost:3306/KhanhDB")
connection = engine.connect()

# Read DB table into dataframe:
df = pd.read_sql_table("Joined_Dataset_final", con=engine)

# Cluster company pairs into different groups with an unique ID, each group has 20 pairs:
numPair = df['pair_id'].max()
print(numPair)
pairID = list(range(1, numPair+1))
random.shuffle(pairID)
clusterID = 1
cluster_df = pd.DataFrame()
for pairIndex in range(20, numPair+1, 20):
    pairList = pairID[pairIndex-20:pairIndex]
    temp_df = df.loc[df['pair_id'].isin(pairList)]
    cluster_df = cluster_df.append(temp_df.assign(cluster_id = clusterID))
    clusterID += 1
    print(clusterID)

print(cluster_df)

# Write dataframe into SQL table:
cluster_df.to_sql(name='Joined_Dataset_clustered', con=engine, index=False, if_exists='replace')
# 185708 rows x 17 columns
