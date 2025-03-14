# -*- coding: utf-8 -*-

########################################################################
###### Authentication page for user: 2 tabs available
###### 1/ Register for new user, 2/ Login for existing user
########################################################################

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user
from sqlalchemy import func, create_engine

import uuid
import datetime
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from app.server import db
from app.services.models import User #import DB table

# THEMES:
app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

### Connecting to a database:
#user_df = pd.read_sql_table("user", con=engine)

# Function to check hash password:
def check_password(password_hash, password):
    return check_password_hash(password_hash, password)

#-----------------------------------------------------------------------------------#
#------------------------------------- LAYOUT --------------------------------------#
#-----------------------------------------------------------------------------------#
# Header:
header = html.Div(
    className='header',
    children=html.Div(
        style={'textAlign': 'center'},
        children=[
            html.Br(),
            # html.Img(
            #     src='https://www.creditshelf.com/img/cs-logo.124e580c.svg',
            #     style={'height':'8%', 'width':'8%'}
            # ),
            html.Div(className='links', children=[
                html.H1('Please login to continue')
            ])
        ]
    )
)

#========== # *** Setting up the tab contents *** # =========#
# Sign-up tab:
tab1_content = dbc.Card(
    dbc.CardBody([
        html.P("New user? Register here:", className="card-text"),
        dbc.Form([
            dbc.FormGroup([
                dbc.Label("Email", className="mr-2"),
                dbc.Input(id="signup_email", type="email", placeholder="Enter email")
            ],
            className="mr-3",
            ),
            dbc.FormGroup([
                dbc.Label("Password", className="mr-2"),
                dbc.Input(id="signup_password", type="password", placeholder="Enter password")
            ],
            className="mr-3",
            ),
            dbc.Button("Submit", color="primary", id="signup-button"),
        ],
        inline=True,
        )]
    ),
    className="mt-3",
)

# Login tab:
tab2_content = dbc.Card(
    dbc.CardBody([
        html.P("Already have an account? Please login:", className="card-text"),
        dbc.Form([
            dbc.FormGroup([
                dbc.Label("Email", className="mr-2"),
                dbc.Input(id="login_email", type="email", placeholder="Enter email")
            ],
            className="mr-3",
            ),
            dbc.FormGroup([
                dbc.Label("Password", className="mr-2"),
                dbc.Input(id="login_password", type="password", placeholder="Enter password")
            ],
            className="mr-3",
            ),
            dbc.Button("Submit", color="primary", id="login-button"),
        ],
        inline=True,
        )]
    ),
    className="mt-3",
)


#========== # *** Displaying the tab layouts *** # =========#
def serve_layout():
    session_id = str(uuid.uuid4())
    return html.Div(
        id='page-content',
        children=[
            html.Div(session_id, id='session-id', style={'display': 'none'}),
            header,

        dbc.Tabs([
            dbc.Tab(tab1_content, label="Sign Up", tab_id="tab-1"),
            dbc.Tab(tab2_content, label="Login", tab_id="tab-2", label_style={"color": "#79c2ad"}),
            ],
            id="tabs",
        ),
        html.Div(id="hidden-div1"),
        html.Div(id="hidden-div2")
        ]
    )

layout = serve_layout


#-----------------------------------------------------------------------------------#
#------------------------------------ CALLBACK -------------------------------------#
#-----------------------------------------------------------------------------------#
# All callbacks should be configure here
def register_callbacks(app):
    #========== # *** Register new user *** # =========#
    @app.callback(
        Output("hidden-div1", "children"),
        [Input("signup-button", "n_clicks")],
        [State("signup_email", "value"), State("signup_password", "value")],
    )
    def register_new_user(n, email, password):
        global user_df
        if n is not None and password is not None and email is not None:
            # if button clicked, add new user to DB:
            user = User.query.filter_by(email = email).first()
            # First check if a user already exists:
            if user:
                return html.Div(
                    'This user already exists. Please login or try to create a new account.',
                    style={'color': '#ff7850', 'marginLeft': 20, 'fontSize': 13})
            else:
                db.session.add(User(
                    email = email,
                    password =  generate_password_hash(password),
                    created_date = datetime.datetime.now()))
                db.session.commit()
                user_df = pd.read_sql_table("user", con=db.engine)
                #return dcc.Location(pathname = "/dashboard", id = 'sucess_register')
                return html.Div(
                            'You have signed up sucessfully! Now login to your account.',
                            style={'color': '#55cc9d', 'marginLeft': 20, 'fontSize': 13})
        if n is not None and (password is None or email is None):
            return html.Div(
                    "Email or password cannot be empty.",
                    style={'color': '#ff7850', 'marginLeft': 20, 'fontSize': 13})

    # #========== # *** Check password and login existing user *** # =========#
    @app.callback(
        Output("hidden-div2", "children"),
        [Input("login-button", "n_clicks")],
        [State("login_email", "value"), State("login_password", "value")]
    )
    def confirm_login(n, email, password):
        if n is not None:
            try:
                user = User.query.filter_by(email = email).first()
                print(user)
                if user is not None:
                    if check_password_hash(user.password, password):
                        login_user(user)
                        return dcc.Location(pathname = "/dashboard", id = 'sucess_login')
                    # password_df = user_df.loc[user_df['email'] == email, 'password'].values[0]
                    # check_value = check_password(password_df, password) 
                    # if check_value == True:
                    #     return dcc.Location(href = "https://www.google.com", id = 'sucess_login')
                    else:
                        return html.Div(
                            'Password is incorrect.',
                            style={'color': '#ff7850', 'marginLeft': 20, 'fontSize': 13})
                else:
                    return html.Div(
                            'Cannot find user.',
                            style={'color': '#ff7850', 'marginLeft': 20, 'fontSize': 13})
                    
            except:
                return html.Div(
                    "Email and Password do not match!",
                    style={'color': '#ff7850', 'marginLeft': 20, 'fontSize': 13})