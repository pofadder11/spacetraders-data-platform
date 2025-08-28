import dash_bootstrap_components as dbc
from dash import Dash

from analytics.schemas.fleet_schema import fleet_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = fleet_layout

if __name__ == "__main__":
    app.run(debug=True)
