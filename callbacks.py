from dash.dependencies import Input, Output
from layout import SPY_CONSTITUENTS as spc, options_layout, stock_layout
from datatable import average_table_callbacks

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
        
    @app.callback(
        Output('selected-ticker', 'children'),
        Input('spx-constituents-dd', 'value'),
        prevent_initial_call=True,
    )
    def update_output(value):
        if not value :
            return ''
        
        ticker = spc['Symbol'][spc['Security'].index(value)]
        full_ticker = f'{ticker} US Equity'
        return  full_ticker
    
    app.clientside_callback(
        """
        function(ticker) {
            return window.dash_clientside.data_utils.get_api_data(ticker);
        }
        """,
        Output('ticker-eod-data', 'data'),
        Input('selected-ticker', 'children'),
        prevent_initial_call=True,
    )
    

    

    
