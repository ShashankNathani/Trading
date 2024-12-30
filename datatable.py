from dash import dcc, html, Input, Output, State, ctx, MATCH
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import datetime 


def average_table_layout() :
    """
    Creates an html.Table with each cell having a unique ID based on row and column indices.
    """
    rows = 3
    cols = 4
    table_rows = []
    colnames = ["Start Date","End Date","Average Window","Average Returns"]
    
    for row_index in range(rows):
        row_cells = []
        for col_index in range(cols):
            cell_id = {'type':'avg-table','row':row_index,'col':col_index}
            if col_index in {0,1}:
                item = dmc.DateInput(id=cell_id,placeholder=f"{colnames[col_index]}",minDate=datetime.date(2005, 1, 1))
            if col_index ==2 :
                item = dcc.Input(id=cell_id,type='number',min=1,step=1)
            if col_index == 3:
                item = html.Div(id=cell_id)
                
            row_cells.append(html.Td(item))
        table_rows.append(html.Tr(row_cells))

    table =  html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in colnames])),
            html.Tbody(table_rows,id='avg-table-contents'),
        ],
        style={"border": "1px solid black", "width": "100%", "borderCollapse": "collapse"},
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
            current_rows = len(table)
            current_cols = len(table[0])

            new_row = []
            for col_index in range(current_cols):
                cell_id = {'type':'avg-table','row':current_rows,'col':col_index}
                if col_index in {0,1}:
                    item = dmc.DateInput(id=cell_id,minDate=datetime.date(2005, 1, 1))                        
                if col_index == 2 :
                    item = dcc.Input(id=cell_id,type='number',min=1,step=1)
                if col_index == 3:
                    item = html.Div(id=cell_id)
                    
                new_row.append(html.Td(item))
            # Create a new row
            # Add the new row to the table
            table.append(html.Tr(new_row))

        return table
    
    app.clientside_callback(
     """
        function(api_data,start_date,end_date,window_size){
            if(!api_data || !start_date || !end_date || !window_size){
                return null ;
            }
            
            console.log('reached here');
            console.log(api_data['data']);
            
            let avg = 100*window.dash_clientside.clients.get_adjusted_close_average(api_data,start_date,end_date,window_size);
            return `${avg.toFixed(2)}%`;
        }
    """,   
    Output({'type':'avg-table','row':MATCH,'col':3}, "children"),
    Input('ticker-eod-data', 'data'),
    Input({'type':'avg-table','row':MATCH,'col':0}, "value"),
    Input({'type':'avg-table','row':MATCH,'col':1}, "value"),
    Input({'type':'avg-table','row':MATCH,'col':2}, "value")
    )
    
