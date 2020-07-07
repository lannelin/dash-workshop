import time

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_caching import Cache

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

CACHE_CONFIG = {
    # using simple instead of setting up redis
    'CACHE_TYPE': 'simple',
}
cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)

app.layout = html.Div([
    html.H6("Personalised greetings - gets your name from the DB"),

    dcc.Input(id='id-input', value="", type='text'),

    html.Br(),
    html.Br(),

    html.Button(id='hello-button', n_clicks=0, children='hello!'),
    html.Div(id='hello-output'),

    html.Br(),

    html.Button(id='goodbye-button', n_clicks=0, children='goodbye!'),
    html.Div(id='goodbye-output'),

])


@cache.memoize()
def get_name(id_val):
    # mimic an expensive operation
    time.sleep(1.5)
    if id_val == "1":
        return "Bob"
    else:
        return "Jim"


@app.callback(
    output=Output(component_id='hello-output', component_property='children'),
    inputs=[Input('hello-button', 'n_clicks')],
    state=[State('id-input', 'value')]
)
def update_hello_div(n_clicks, id_val):
    if id_val is "":
        return "I don't know you!"
    name = get_name(id_val)
    return "hello, {name}".format(name=name)


@app.callback(
    output=Output(component_id='goodbye-output', component_property='children'),
    inputs=[Input('goodbye-button', 'n_clicks')],
    state=[State('id-input', 'value')]
)
def update_goodbye_div(n_clicks, id_val):
    if id_val is "":
        return "I don't know you!"
    name = get_name(id_val)
    return "goodbye, {name}".format(name=name)


if __name__ == '__main__':
    app.run_server(debug=True)
