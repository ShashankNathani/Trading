from dash import dcc, html, Input, Output, State, ctx, MATCH
from data_api import get_sp500_constituents
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import datetime 

COLNAMES = ["Ticker Type","Ticker","Start Date","End Date","Average Window","Average Returns","Probability Chart"]
SPXC = get_sp500_constituents()

def get_table_cell_item(row,col) :
    
    cell_id = {'type':'avg-table','row':row,'col':col}
    if col == 0 :
        item = dcc.Dropdown(id=cell_id,options=['S&P Companies','Custom Tickers'],value='S&P Companies')
    if col == 1 :
        item = html.Div(dcc.Dropdown(id={'type':'ticker-input','row':row,'col':col},options=SPXC['Security']),id=cell_id)
    if col in {2,3}:
        item = dmc.DateInput(id=cell_id,placeholder=f"{COLNAMES[col]}",minDate=datetime.date(2005, 1, 1))
    if col == 4 :
        item = dcc.Input(id=cell_id,type='number',min=1,step=1)
    if col == 5:
        item = html.Div(id=cell_id)
    if col == 6:
        plot_dimension =  {"width": "1000px", "height": "600px"} 
        item1 = dbc.Button(html.I(className="bi bi-bar-chart-line"),id=cell_id,outline=True, color="dark")
        item2 = dbc.Modal(dbc.ModalBody(dcc.Graph(id={'type':'dist-chart','row':row},style=plot_dimension)),id={'type':'chart-modal','row':row})
        item = [item1,item2]
        
    return item


def average_table_layout() :
    """
    Creates an html.Table with each cell having a unique ID based on row and column indices.
    """
    rows = 3
    cols = len(COLNAMES)
    table_rows = []
    cell_width = 100//cols
    
    for row_index in range(rows):
        ticker_store = dcc.Store(id={'row':row_index,'type':'ticker-eod-data'})
        row_cells = [ticker_store]
        for col_index in range(cols):
            item = get_table_cell_item(row_index,col_index)
            row_cells.append(html.Td(item,style={"width": f"{cell_width}%"}))
        table_rows.append(html.Tr(row_cells))

    table =  html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in COLNAMES])),
            html.Tbody(table_rows,id='avg-table-contents'),
        ],
        style={"border": "1px solid black", "width": "2000px", "borderCollapse": "collapse"},
    )
    
    layout =  html.Div(
                [
                    html.Div(id="table-container", children=table,style={'width':'40%'}),
                    dbc.Button("Add Row", id="add-row-button", color="primary", style={"marginTop": "10px"}),
                    dbc.Button("Delete Row", id="delete-row-button", color="primary", style={"marginTop": "10px"}),
                ]
            )

    return layout
    
# Layout with table and button
def average_table_callbacks(app) :

# Callback to dynamically add rows to the table
    @app.callback(
        Output("avg-table-contents", "children"),
        Input("add-row-button", "n_clicks"),
        Input("delete-row-button", "n_clicks"),
        State("avg-table-contents", "children"),
        prevent_initial_call=True,
    )
    def add_row(n1,n2, table):
        """
        Adds and deletes row to the table when the button is clicked.
        """
        # Get the current number of rows from the table
        
        if 'delete-row-button.n_clicks' in ctx.triggered_prop_ids:
            table.pop()
        
        if 'add-row-button.n_clicks' in ctx.triggered_prop_ids:
            current_row = len(table)
            current_cols = len(COLNAMES)
            ticker_store = dcc.Store(id={'row':current_row,'type':'ticker-eod-data'})
            new_row = [ticker_store]
            for col_index in range(current_cols):
                item = get_table_cell_item(current_row,col_index)
                new_row.append(html.Td(item))
            # Create a new row
            # Add the new row to the table
            table.append(html.Tr(new_row))

        return table
    
    app.clientside_callback(
     """
        function(api_data,start_date,end_date,window_size){
            if(!api_data || !start_date || !end_date || !window_size){
                return window.dash_clientside.no_update ;
            }
            
            let moving_window_returns = window.dash_clientside.data_utils.get_adjusted_close_returns(api_data,start_date,end_date,window_size);
            let avg_returns = 100*window.dash_clientside.data_utils.average(moving_window_returns);
                        
            return `${avg_returns.toFixed(2)}%`;
        }
    """,   
    Output({'type':'avg-table','row':MATCH,'col':5}, "children"),
    Input({'type':'ticker-eod-data','row':MATCH},'data'),
    Input({'type':'avg-table','row':MATCH,'col':2}, "value"),
    Input({'type':'avg-table','row':MATCH,'col':3}, "value"),
    Input({'type':'avg-table','row':MATCH,'col':4}, "value"),
    )
    
    @app.callback(
        Output({'type':'chart-modal','row':MATCH}, "is_open"),
        Input({'type':'avg-table','row':MATCH,'col':6}, "n_clicks"),
        State({'type':'chart-modal','row':MATCH}, "is_open"),
        prevent_initial_call=True,
    )
    def open_dist_modal(n_clicks,is_open):
        if n_clicks :
            return not is_open
    
    app.clientside_callback(
        """
        function(is_open,api_data,start_date,end_date,window_size,id) {
            if(!api_data || !start_date || !end_date || !window_size || !is_open){
                return window.dash_clientside.no_update ; 
            }
            
            let elem_id = JSON.stringify({'row':id['row'],'type':'dist-chart'});
            let elem0 = document.getElementById(JSON.stringify(elem_id));
            
            console.log(elem0);
            
            let moving_window_returns = window.dash_clientside.data_utils.get_adjusted_close_returns(api_data,start_date,end_date,window_size);
            return window.dash_clientside.chart_utils.createCumulativeDistributionChart(moving_window_returns,elem_id);
        }
        """,
        Output({'type':'dist-chart','row':MATCH}, 'figure'),
        Input({'type':'chart-modal','row':MATCH}, "is_open"),
        State({'type':'ticker-eod-data','row':MATCH},'data'),
        State({'type':'avg-table','row':MATCH,'col':2}, "value"),
        State({'type':'avg-table','row':MATCH,'col':3}, "value"),
        State({'type':'avg-table','row':MATCH,'col':4}, "value"),
        State({'type':'dist-chart','row':MATCH}, 'id'),    
    )
    
    @app.callback(
        Output({'type':'avg-table','row':MATCH,'col':1},'children'),
        Input({'type':'avg-table','row':MATCH,'col':0},'value'),
        State({'type':'avg-table','row':MATCH,'col':1},'id'),
    )
    def display_ticker_input(value,id):
        
        cell_id = {'type':'ticker-input','row':id['row'],'col':id['col']}
        
        if value == 'S&P Companies':
            item =  dcc.Dropdown(
                id=cell_id,
                options=SPXC['Security'],
            )
            
            return item
            
        if value == 'Custom Tickers':
            
            return dcc.Input(
                    id=cell_id,
                    type='text',
                    placeholder='Enter a ticker symbol',
                )
        
    
    app.clientside_callback(
        """
        function(ticker_input,ticker_type,sp_store) {
            
            if(!ticker_input || !ticker_type){
                return window.dash_clientside.no_update;
            }
            
            let selected_ticker;
            
            if(ticker_type == 'S&P Companies'){
                selected_ticker = sp_store[ticker_input];
            }else{
                selected_ticker = ticker_input;
            }
            
            return window.dash_clientside.data_utils.get_api_data(selected_ticker);
        }
        """,
        Output({'type':'ticker-eod-data','row':MATCH},'data'),
        Input({'type':'ticker-input','row':MATCH,'col':1},'value'),
        State({'type':'avg-table','row':MATCH,'col':0},'value'),
        State('sp500-data','data'),
        prevent_initial_call=True,
    )