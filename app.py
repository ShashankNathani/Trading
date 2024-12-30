import dash
from dash import _dash_renderer
from layout import app_layout
from callbacks import app_callbacks
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
# Initialize the Dash app
_dash_renderer._set_react_version("18.2.0")
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,dmc.styles.ALL])
app.layout = dmc.MantineProvider(app_layout())

app_callbacks(app)
# Define the layout of the app
if __name__ == '__main__':
    app.run_server(debug=True)