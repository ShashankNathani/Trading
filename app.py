import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from layout import app_layout

# Initialize the Dash app
def initialize() :
    
    app = dash.Dash(__name__)
    app.layout = app_layout()

# Define the layout of the app
if __name__ == '__main__':
    app.run_server(debug=True)