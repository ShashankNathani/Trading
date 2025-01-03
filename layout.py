from dash import dcc, html
from dash.dependencies import Input, Output
from data_api import get_sp500_constituents
from datatable import average_table_layout
import dash_bootstrap_components as dbc

spc = get_sp500_constituents()

def options_layout() :
    return []


def stock_layout() :
    
    layout = html.Div([
                html.Div(
                    children = [
                        html.Div(style={'widht':'100%','height':'25px'}),
                        dcc.Dropdown(
                            id='stock-type-dd',
                            options=['S&P Companies','Custom Tickers'],
                            style={
                                'display':'inline-block',
                                'width':'300px',
                            },
                            value='S&P Companies'
                        ),
                        html.Div(
                            id='ticker-input-div',
                            style = {
                                'display':'inline-block',
                                'width':'300px',
                                'maxHeight': '1000px',
                                'marginRight':'20px'
                            },
                            children = [dcc.Dropdown(id='ticker-input',options=spc['Security'])]
                        ),
                        html.Div([],id='selected-ticker',style={'display':'none'}),
                        dbc.Button('Submit', id='submit-ticker',style={'display':'none'},color="success")                        
                    ]
                ),

                html.Div(id='output-container'),
                average_table_layout(),
                dcc.Store(id="ticker-eod-data"),
                html.Div(dcc.Graph('dummy-to-let-plotlyjs-work'),style={'display':'none'})
            ])

    return layout

def app_layout():
    layout = html.Div([
        dbc.Tabs(
            [
                dbc.Tab(label="Stocks", tab_id="stocks"),
                dbc.Tab(label="Options", tab_id="options"),
            ],
            id="tabs",
            active_tab="stocks",
        ),
        html.Div(id="tab-content",children=stock_layout()),
    ])
    
    return layout
            
    