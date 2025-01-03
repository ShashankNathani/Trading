from dash import dcc, Input, Output, State, no_update
from layout import options_layout, stock_layout
from datatable import average_table_callbacks
import dash_bootstrap_components as dbc


OPTIONS_LAYOUT = options_layout()
STOCKs_LAYOUT = stock_layout()

def app_callbacks(app) :
    
    average_table_callbacks(app)
    
    @app.callback(
        Output('tab-content', 'children'),
        Input('tabs', 'active_tab'),
        prevent_initial_call=True,
    )
    def update_tab_content(value):
        if value == 'stocks':
            return STOCKs_LAYOUT
        elif value == 'options':
            return OPTIONS_LAYOUT
        else:
            return 'No layout found'
        
    

    

    

    
