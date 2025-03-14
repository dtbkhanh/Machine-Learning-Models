import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import uuid

session_id = str(uuid.uuid4())

layout = html.Div([
    html.Div(session_id, id='session-id', style={'display': 'none'}),
    html.H1('SARA V0.1 Companies'),
    html.Div(
        id='frame1',
        children = 'no click'
    ),
    html.Div(
                style={'textAlign': 'center'},
                children=[
                    dbc.Button(
                        'button1', 
                        color = "primary", size="lg", id='button1', className="mr-1"),
                    dbc.Button(
                        'button2',
                        color = "primary", size="lg", id='button2', className="mr-1"),  
            ])
])


# All callbacks should be configure here
def register_callbacks(dash_app):
    # pass
    @dash_app.callback(
        Output('frame1', 'children'),
        [Input('button1', 'n_clicks')]
    )
    def capture_1(n1):
        if n1 is not None:
            return 'button clicked'
