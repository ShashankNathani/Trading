from dash import dcc, Input, Output, State, no_update
from layout import spc, options_layout, stock_layout
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
        
    
    @app.callback(
        Output('ticker-input-div', 'children'),
        Output('selected-ticker', 'style'),
        Output('submit-ticker', 'style'),
        Input('stock-type-dd', 'value'),
    )
    def display_ticker_input(value):
        
        style = {'display':'inline-block','width':'300px','marginBottom':'5px'}
        hidden_style = {'display':'none'}
        
        if value == 'S&P Companies':
            item =  dcc.Dropdown(
                id='ticker-input',
                options=spc['Security'],
            )
            
            return item, style, hidden_style
            
        if value == 'Custom Tickers':
            
            item =  dcc.Input(
                    id='ticker-input',
                    type='text',
                    placeholder='Enter a ticker symbol',
                    style={'display':'inline-block'}
                )
            
            return item, hidden_style, style
        
    @app.callback(
        Output('selected-ticker', 'children'),
        Input('ticker-input', 'value'),
        State('stock-type-dd', 'value'),
        prevent_initial_call=True,
    )
    def update_output(value,stock_type):
        
        if not value or stock_type != 'S&P Companies' :
            return ''
        else :
            ticker = spc['Symbol'][spc['Security'].index(value)]
            full_ticker = f'{ticker} US Equity'
            return  full_ticker

    
    app.clientside_callback(
        """
        function(ticker_dd, n_clicks, stock_type, ticker_input) {
            
            if((stock_type == 'S&P Companies' && !ticker_dd) || (stock_type == 'Custom Tickers' && !n_clicks)){
                return window.dash_clientside.no_update;
            }
            
            let selected_ticker;
            
            if(stock_type == 'Custom Tickers'){
                selected_ticker = ticker_input;
            }
            
            if(stock_type == 'S&P Companies'){
                selected_ticker = ticker_dd;
            }
            
            console.log(selected_ticker);
            
            return window.dash_clientside.data_utils.get_api_data(selected_ticker);
        }
        """,
        Output('ticker-eod-data', 'data'),
        Input('selected-ticker', 'children'),
        Input('submit-ticker', 'n_clicks'),
        State('stock-type-dd', 'value'),
        State('ticker-input', 'value'),
        prevent_initial_call=True,
    )
    

    

    
