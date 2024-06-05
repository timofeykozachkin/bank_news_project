import dash
import dash_bootstrap_components as dbc
from components import layout, callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
layout.add_layout(app)
callbacks.add_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)
