from dash import dcc, html
from dash.dependencies import Input, Output
from yf_data import get_sp500_constituents

SPY_CONSTITUENTS = get_sp500_constituents()

def app_layout() :
    
    layout = html.Div([
                html.Div(
                    html.H1('S&P 500 Constituents'),
                    style={'width':'100%'}                   
                ),
                dcc.Dropdown(
                    id='spx-constituents',
                    options=[
                        {'label': 'Option 1', 'value': '1'},
                        {'label': 'Option 2', 'value': '2'},
                        {'label': 'Option 3', 'value': '3'}
                    ],
                    value='1',
                    style = {'width':'300px'}# Default value
                ),
                html.Div(id='output-container')
            ])

    return layout
            
    