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
    cols = 5
    table_rows = []
    colnames = ["Start Date","End Date","Average Window","Average Returns","Probability Chart"]
    
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
            if col_index == 4:
                plot_dimension =  {"width": "1000px", "height": "600px"} 
                item1 = dbc.Button(html.I(className="bi bi-bar-chart-line"),id=cell_id,outline=True, color="dark")
                item2 = dbc.Modal(dbc.ModalBody(dcc.Graph(id={'type':'dist-chart','row':row_index},style=plot_dimension)),id={'type':'chart-modal','row':row_index})
                item = [item1,item2]
                
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
            current_row = len(table)
            current_cols = len(table[0])

            new_row = []
            for col_index in range(current_cols):
                cell_id = {'type':'avg-table','row':current_row,'col':col_index}
                if col_index in {0,1}:
                    item = dmc.DateInput(id=cell_id,minDate=datetime.date(2005, 1, 1))                        
                if col_index == 2 :
                    item = dcc.Input(id=cell_id,type='number',min=1,step=1)
                if col_index == 3:
                    item = html.Div(id=cell_id)
                if col_index == 4:
                    plot_dimension =  {"width": "1000px", "height": "600px"}
                    item1 = dbc.Button(html.I(className="bi bi-bar-chart-line"),id=cell_id,outline=True, color="dark")
                    item2 = dbc.Modal(dbc.ModalBody(dcc.Graph(id={'type':'dist-chart','row':current_row},style=plot_dimension)),id={'type':'chart-modal','row':current_row})
                    item = [item1,item2]
                    
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
    Output({'type':'avg-table','row':MATCH,'col':3}, "children"),
    Input('ticker-eod-data', 'data'),
    Input({'type':'avg-table','row':MATCH,'col':0}, "value"),
    Input({'type':'avg-table','row':MATCH,'col':1}, "value"),
    Input({'type':'avg-table','row':MATCH,'col':2}, "value"),
    )
    
    @app.callback(
        Output({'type':'chart-modal','row':MATCH}, "is_open"),
        Input({'type':'avg-table','row':MATCH,'col':4}, "n_clicks"),
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
            return window.dash_clientside.chart_utils.createProbabilityDistributionChart(moving_window_returns,elem_id);
        }
        """,
        Output({'type':'dist-chart','row':MATCH}, 'figure'),
        Input({'type':'chart-modal','row':MATCH}, "is_open"),
        State('ticker-eod-data', 'data'),
        State({'type':'avg-table','row':MATCH,'col':0}, "value"),
        State({'type':'avg-table','row':MATCH,'col':1}, "value"),
        State({'type':'avg-table','row':MATCH,'col':2}, "value"),
        State({'type':'dist-chart','row':MATCH}, 'id'),    
    )
    
