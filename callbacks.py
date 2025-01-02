from dash.dependencies import Input, Output
from layout import SPY_CONSTITUENTS as spc
from datatable import average_table_callbacks

def app_callbacks(app) :
    
    average_table_callbacks(app)

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
    )
    

    
