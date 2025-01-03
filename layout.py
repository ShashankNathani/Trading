from dash import dcc, html
from dash.dependencies import Input, Output
from data_api import get_sp500_constituents
from datatable import average_table_layout
import dash_bootstrap_components as dbc

def store_sp500_constituents() :
    spxc = get_sp500_constituents()
    store = {}
    for i in range(len(spxc['Symbol'])):
        store[spxc['Security'][i]] = spxc['Symbol'][i]

    return dcc.Store(id='sp500-data',data=store)

def options_layout() :
    return []


def stock_layout() :
    
    layout = html.Div([
                html.Div(style={'width':'100%','height':'25px'}),
                store_sp500_constituents(),
                average_table_layout(),
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
            
    