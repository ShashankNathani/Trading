from dash import dcc, html
from dash.dependencies import Input, Output
from data_api import get_sp500_constituents
import dash_table
from datatable import average_table_layout

SPY_CONSTITUENTS = get_sp500_constituents()



def app_layout() :
    
    layout = html.Div([
                html.Div(
                    html.H1('S&P 500 Constituents'),
                    style={'width':'100%'}                   
                ),
                html.Div(
                    children = [
                        dcc.Dropdown(
                            id='spx-constituents-dd',
                            options=SPY_CONSTITUENTS['Security'],
                            value='1',
                            style = {
                                'display':'inline-block',
                                'width':'300px',
                                'maxHeight': '1000px',
                                'marginRight':'100px'
                            }
                        ),
                        html.Div([],id='selected-ticker',style={'display':'inline-block','width':'300px'})
                    ]
            ),
                html.Div(id='output-container'),
                average_table_layout(),
                dcc.Store(id="ticker-eod-data"),
        ])

    return layout
            
    