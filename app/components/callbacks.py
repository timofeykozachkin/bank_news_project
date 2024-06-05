from dash import html, Input, Output, State, no_update, dash_table
from utils.lstm_predict import preprocess_stock_data
from utils.bert import bert_query
# from app.components.layout import add_layout


def add_callback(app):
    @app.callback(
        Output('prediction-val-table', 'children'),
        Input('predict-button', 'n_clicks'),
        State('my-dynamic-dropdown', 'value'),
        State('input-news', 'value')
    )
    def update_graph(n_clicks, stock_name, news_text):
        if n_clicks > 0 and stock_name is not None and news_text is not None:
            # file_path = os.path.join('app', 'data', selected_file)

            sent_label, sent_score = bert_query({
                "inputs": [news_text],
            })
            if sent_label in ('LABEL_0', 'LABEL_3'):
                sent_score *= (-1)
            elif sent_label == 'LABEL_1':
                sent_score = 0

            future_price, pred_cat = preprocess_stock_data(stock_name, sent_score)

            columns = [dict(id='indicator', name='indicator', type='text'),
                       dict(id='value', name='value', type='numeric'),
                       dict(id='direction', name='direction', type='text')]
            data = [{'indicator': 'Stock price', 'value': round(future_price, 4), 'direction': pred_cat},
                    {'indicator': 'ROE', 'value': 10.4, 'direction': '↓ down'},
                    {'indicator': 'ROA', 'value': 16.7, 'direction': '↓ down'},
                    {'indicator': 'Net Assets Ratio', 'value': 9.8, 'direction': '↓ down'}]
            html_table = html.Div(dash_table.DataTable(data=data,
                                                       columns=columns,
                                                       style_header={'display': 'none'},
                                                       style_cell={'textAlign': 'center'}))

            return html_table
        return no_update

    @app.callback(
        Output('input-news', 'value', allow_duplicate=True),
        Input('button-item1', 'n_clicks'),
        State('button-item1', 'children'),
        prevent_initial_call='initial_duplicate'
    )
    def update_news_text(n_clicks, but_text):
        if n_clicks > 0:
            return but_text
        return no_update

    @app.callback(
        Output('input-news', 'value', allow_duplicate=True),
        Input('button-item2', 'n_clicks'),
        State('button-item2', 'children'),
        prevent_initial_call='initial_duplicate'
    )
    def update_news_text(n_clicks, but_text):
        if n_clicks > 0:
            return but_text
        return no_update

    @app.callback(
        Output('input-news', 'value', allow_duplicate=True),
        Input('button-item3', 'n_clicks'),
        State('button-item3', 'children'),
        prevent_initial_call='initial_duplicate'
    )
    def update_news_text(n_clicks, but_text):
        if n_clicks > 0:
            return but_text
        return no_update

    # @app.callback(
    #     Output("my-dynamic-dropdown", "options"),
    #     Input("my-dynamic-dropdown", "search_value")
    # )
    # def update_options(search_value):
    #     if not search_value:
    #         raise PreventUpdate
    #     return [o for o in options if search_value in o["label"]]
