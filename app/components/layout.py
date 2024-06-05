import dash_bootstrap_components as dbc
from dash import dcc, html


def add_layout(app):
    options = [{'label': 'SBER', 'value': 'SBER'},
               {'label': 'VTBR', 'value': 'VTBR'},
               {'label': 'BSPB', 'value': 'BSPB'}]

    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Банки. Прогнозы", style={'textAlign': 'center', 'margin-top': '20px'})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Input(
                    id="input-news",
                    type='text',
                    placeholder="введите текст новости",
                    style={'width': 830}
                )
            ], width=6, style={'margin-top': '20px'}),
            dbc.Col([
                html.Div(dcc.Dropdown(id="my-dynamic-dropdown", options=options)),
            ], width=4, style={'margin-top': '20px'}),
            dbc.Col([
                html.Button('Прогноз', id='predict-button', n_clicks=0, className='btn btn-primary'),
            ], width=2, style={'margin-top': '20px'})
        ]),

        dbc.Row([
            dbc.Col([
                html.Div(
                    dbc.ListGroup([
                        dbc.ListGroupItem("Все очень хорошо", id="button-item1", n_clicks=0, action=True),
                        dbc.ListGroupItem("Сбербанк плохо обошелся с клиентом", id="button-item2",
                                          n_clicks=0, action=True),
                        dbc.ListGroupItem("Все плохо", id="button-item3", n_clicks=0, action=True)],
                        id='news-buttons')
                )], width=6, style={'margin-top': '58px'}),
            dbc.Col([
                html.Center('ПРОГНОЗЫ', style={'text-align': 'center', 'margin-top': '10px'}),
                html.Div(id='prediction-val-table')
            ], width=5)
        ])], fluid=True)
