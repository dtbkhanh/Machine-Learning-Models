# -*- coding: utf-8 -*-

########################################################################
###### Simple UI with 2 tables displayed and 2 interactive buttons
###### Button-click with captured action and stored timestamp into DB
########################################################################

import dash
import logging
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, create_engine
from flask_login import logout_user, current_user

from app.server import db

import datetime
import dash_table
import pandas as pd
import numpy as np
import time
import uuid
import random

from services.models import ActionCapture #import DB table
from app.server import db
from app.utils import get_db_url

#=====================Global Variables====================#
button1_click = 0
button2_click = 0
#=========================================================#

# THEMES:
dash_app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

### Connecting to a database:
# dash_app.server.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:helloworld@localhost:3306/KhanhDB"
# engine = create_engine(dash_app.server.config["SQLALCHEMY_DATABASE_URI"])
# db = SQLAlchemy(dash_app.server)
# logging.info(db)
#-----------------------------------------------------------------------------------#
#----------------------------------- DATAFRAME -------------------------------------#
#-----------------------------------------------------------------------------------#

# Read DB table into dataframe:
df = pd.read_sql_table("Joined_Dataset_clustered", con=db.engine)

data_df = df.loc[(df['cluster_id'] == 1) | (df['cluster_id'] == 2) | (df['cluster_id'] == 3)] #This will change every voting session
pairList = data_df['pair_id'].to_list()
pairList = list(dict.fromkeys(pairList)) #remove duplicates
numPair = len(pairList)
pairIndex = 0
temp_df = data_df.loc[df['pair_id'] == pairList[pairIndex]]
df1 = temp_df.iloc[:, 0:8]
df2 = temp_df.iloc[:, 8:]


#-----------------------------------------------------------------------------------#
#------------------------------------- LAYOUT --------------------------------------#
#-----------------------------------------------------------------------------------#

# Show currency units (Million euros)
def currency_convert(col):
    result = '€' + str(col)
    return result

# Show '%' symbols:
def show_percentage(col):
    result = str(col) + '%'
    return result

# Add extra columns to dataframe:
def add_columns(df):
    df["EBITDA"] = df["Depreciation and Amortization"].astype(float) + df["Operating Profits"].astype(float)
    df["EBITDA"] = df["EBITDA"].round(5)

    df["Net Profit"] = df["Operating Profits"].astype(float) - df["Interest Expense"].astype(float)
    df["Net Profit"] = df["Net Profit"].round(5)

    df["EBITDA %"] = df["EBITDA"].astype(float)/ df["Revenues"].astype(float) * 100
    df["EBITDA %"] = df["EBITDA %"].round(4)

    df["Op Prof %"] = df["Operating Profits"].astype(float)/ df["Revenues"].astype(float) * 100
    df["Op Prof %"] = df["Op Prof %"].round(4)

    df["Op Prof Growth"] = (df["Op Prof %"].astype(float)/df["Op Prof %"].shift(1).astype(float)) - 1
    df["Op Prof Growth"] = df["Op Prof Growth"].round(4)
    df["Op Prof Growth"] = df["Op Prof Growth"].fillna(0)

    df["Rev growth"] = ((df["Revenues"].astype(float)/df["Revenues"].shift(1).astype(float)) - 1) * 100
    df["Rev growth"] = df["Rev growth"].round(4)
    df["Rev growth"] = df["Rev growth"].fillna(0)

    df["Net Profit %"] = df["Net Profit"].astype(float)/ df["Revenues"].astype(float) * 100
    df["Net Profit %"] = df["Net Profit %"].round(4)
    

# Function to generate table:
def generate_table(dataframe):
    dataframe = dataframe.drop(dataframe.filter(regex='id').columns, axis=1) # drop ID columns
    dataframe = dataframe.rename(columns={"company_name_1": "Company Name", 
                                            "year_1": "Year", 
                                            "revenue_1": "Revenues", 
                                            "depreciation_amortization_1": "Depreciation and Amortization", 
                                            "operating_profit_1": "Operating Profits", 
                                            "interest_expense_1": "Interest Expense"})
    dataframe = dataframe.rename(columns = {"company_name_2": "Company Name", 
                                            "year_2": "Year", 
                                            "revenue_2": "Revenues", 
                                            "depreciation_amortization_2": "Depreciation and Amortization", 
                                            "operating_profit_2": "Operating Profits", 
                                            "interest_expense_2": "Interest Expense"})
    add_columns(dataframe)
    # Add currency unit:
    for i in range(2, 8):
        name = dataframe.columns[i]
        dataframe[name] = dataframe.apply(lambda x: currency_convert(x.iloc[i]), axis=1)

    # Add '%' symbol:
    for i in range(8, len(dataframe.columns)):
        name = dataframe.columns[i]
        dataframe[name] = dataframe.apply(lambda x: show_percentage(x.iloc[i]), axis=1)

    return dbc.Table.from_dataframe( 
        dataframe,
        striped = True, bordered = True, hover = True,
        style={'height': '300', 'text-align': 'right', 'font_size': '26px',})



#========== # *** Function to setup the layout *** # =========#
def serve_layout():
    session_id = str(uuid.uuid4())

    return html.Div([
        html.Div(session_id, id='session-id', style={'display': 'none'}),
        
        # Header:
        html.Br(),
        html.H1(children='Financial dataset', style={'textAlign': 'center'}),
        html.H5(children='(Millions Euros)', style={'textAlign': 'center'}),
        html.Br(),
        html.Div(
            style={'textAlign': 'center'},
            children=[
                dbc.Button("Logout", size="sm", color="danger", id='logout_button')
            ]),

        html.Hr(),
        # html.Div(
        #     style={"overflow": "hidden"},
        #     children=[
        #         html.Div(
        #             id='frame1',
        #             style={"width": "48%", "float": "left", 'text-align': 'center', 'height': '480px'}, 
        #             children = generate_table(df1)
        #         ),
        #         html.Div(
        #             id='frame2',
        #             style={"width": "48%", "float": "right", 'text-align': 'center', 'height': '480px'}, 
        #             children = generate_table(df2)
        #         )
        #     ]
        # ),
        # Print two dataframe tables:
        html.H6(children='Company 1:', style={'textAlign': 'left', 'marginLeft': 20, 'font-weight': 'bold'}),
        html.Div(
            id='frame1',
            style={"float": "center", 'textAlign': 'center', 'marginLeft': 20, 'marginRight': 20}, 
            children = generate_table(df1)
        ),

        html.Br(),
        html.H6(children='Company 2:', style={'textAlign': 'left', 'marginLeft': 20, 'font-weight': 'bold'}),
        html.Div(
            id='frame2',
            style={"float": "center", 'textAlign': 'center', 'marginLeft': 20, 'marginRight': 20}, 
            children = generate_table(df2)
        ),

        # Print two comparing buttons:
        dbc.Jumbotron([
            html.H4('Which company would rank better?', style={'textAlign': 'center'}),
            html.Hr(className="my-2"),
            html.Div(
                style={'textAlign': 'center'},
                children=[
                    dbc.Button(
                        str(df1.iloc[0, 2]), 
                        color = "primary", size="lg", id='button1', className="mr-1"),
                    dbc.Button(
                        str(df2.iloc[1, 1]),
                        color = "primary", size="lg", id='button2', className="mr-1"),
                    html.Br(),
                    html.Div(id='output-1'),
            ]),
        ]),

        # Hidden Divs:
        html.Div(id='output-3'),

        # Print total ranking button and display ranking list:
        html.Div(
             style={'textAlign': 'center'},
             children=[
                dbc.Button("Total Ranking", id="rank-button", size="lg", color="secondary"),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Total Ranking"),
                        dbc.ModalBody(id='output-rank'),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Close", id="close-centered", className="ml-auto"
                            )
                        ),
                    ],
                    id="modal-centered",
                    size="xl",
                    centered=True,
                    scrollable=True
                )],
        ),    
    ])

layout = serve_layout


#-----------------------------------------------------------------------------------#
#------------------------------------ CALLBACK -------------------------------------#
#-----------------------------------------------------------------------------------#
# All callbacks should be configure here
def register_callbacks(dash_app):
    #========== # *** LOGOUT button *** # =========#
    @dash_app.callback(
        Output('output-3', "children"), 
        [Input("logout_button", "n_clicks")]
    )
    def logout_button_click(n):
        if n is not None:
            global pairIndex
            global button1_click
            global button2_click
            logout_user()
            pairIndex = 0
            button1_click = 0
            button2_click = 0
            return dcc.Location(pathname = "/login", id = 'login2')

    #========== # *** COMPARING BUTTONS click: *** # =========#
    @dash_app.callback(
        [Output('frame1', 'children'),
        Output('frame2', 'children'),
        Output('button1', 'children'),
        Output('button2', 'children'),
        Output('output-1', 'children')],       
        [Input('button1', 'n_clicks'),
        Input('button2', 'n_clicks')]
    )
    def capture_1(n1, n2):
        global pairIndex
        global df1
        global df2
        global button1_click
        global button2_click

        if n1 is None:
            n1 = 0
        if n2 is None:
            n2 = 0

        # When not click both buttons:
        # if n1 is None and n2 is None:
        #     return generate_table(df1), 
        #     generate_table(df2),
        #     str(df1.iloc[0, 2]), #button 1's text
        #     str(df2.iloc[1, 1]),  #button 2's text
        #     html.Div('You have completed "{}"/ 252 votes'.format(0))
        # else:
        # When only button 1 is clicked: 
        if n1 != 0:
            if n1 > button1_click:
                button1_click = n1
                print('button1 clicked')
                # Update into table action_capture inside DB:
                db.session.add(ActionCapture(
                    pair_id = str(df1.iloc[0, 0]),
                    company_id_voted = str(df1.iloc[0, 1]),
                    company_name_voted = str(df1.iloc[0, 2]), 
                    company_id_compared = str(df2.iloc[0, 0]),
                    company_name_compared = str(df2.iloc[0, 1]),
                    button1_clicked = 1,
                    user = current_user.id,
                    timestamp = datetime.datetime.now()))
                db.session.commit()

        # When only button 2 is clicked: 
        if n2 != 0:
            if n2 > button2_click:
                button2_click = n2
                print('button2 clicked')
                # Update into table action_capture inside DB:
                db.session.add(ActionCapture(
                    pair_id = str(df1.iloc[0, 0]),
                    company_id_voted = str(df2.iloc[0, 0]),
                    company_name_voted = str(df2.iloc[0, 1]),
                    company_id_compared = str(df1.iloc[0, 1]),
                    company_name_compared = str(df1.iloc[0, 2]),
                    button1_clicked = 0,
                    user = current_user.id,
                    timestamp = datetime.datetime.now()))          
                db.session.commit()

        # Whenever a button is clicked, both dataframe tables will be updated:
        if pairIndex < numPair-1:
            pairIndex += 1
            temp_df = data_df.loc[df['pair_id'] == pairList[pairIndex]]
            df1 = temp_df.iloc[:, 0:8]
            df2 = temp_df.iloc[:, 8:]
            n_total = n1 + n2
            return generate_table(df1), generate_table(df2),str(df1.iloc[0, 2]), str(df2.iloc[1, 1]), html.Div('You have completed {}/ 251 votes'.format(n_total))
        else:
            logout_user()
            pairIndex = 0
            button1_click = 0
            button2_click = 0
            return dcc.Location(pathname = "/login", id = 'login'),'','','',''


    #========== # *** TOTAL RANKING Modal *** # =========#
    @dash_app.callback(
        [Output('modal-centered', 'is_open'), Output('output-rank', 'children')],
        [Input('rank-button', 'n_clicks'), Input('close-centered', 'n_clicks')],
        [State('modal-centered', 'is_open')],
    )
    def toggle_modal(n1, n2, is_open):
        query = db.session.query(
            ActionCapture.company_name_voted,
            func.count(ActionCapture.company_name_voted)
        ).group_by(ActionCapture.company_name_voted).order_by(func.count(ActionCapture.company_name_voted).desc()).all()
        if n1 or n2:
            temp = []
            j = 1
            for i in query:
                tempStr = str(j) + '. ' + i[0] + ' - ' + str(i[1]) + ' votes'
                temp.append(html.P(tempStr))
                j += 1
            return not is_open, temp
        return is_open, ''