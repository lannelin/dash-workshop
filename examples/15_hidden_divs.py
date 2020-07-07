import time

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H6("Personalised greetings - gets your name from the DB"),

    dcc.Input(id='id-input', value="0", type='text'),
    html.Button(id='name-button', n_clicks=0, children='get name'),
    html.Div(id='name-output'),
    # hidden div!
    html.Div(id='hidden-output', style={"display": "none"}),

    html.Br(),
    html.Br(),

    html.Button(id='hello-button', n_clicks=0, children='hello!'),
    html.Div(id='hello-output'),

    html.Br(),

    html.Button(id='goodbye-button', n_clicks=0, children='goodbye!'),
    html.Div(id='goodbye-output'),

])


def get_name(id_val):
    # mimic an expensive operation
    time.sleep(1.5)
    if id_val == "1":
        return "Bob"
    else:
        return "Jim"


@app.callback(
    output=[
        Output(component_id='name-output', component_property='children'),
        Output(component_id='hidden-output', component_property='children')
    ],
    inputs=[Input('name-button', 'n_clicks')],
    state=[State('id-input', 'value')]
)
def update_name(n_clicks, id_val):
    t0 = time.time()

    if n_clicks == 0:
        return None, None

    # no more global
    name = get_name(id_val)

    time_taken = time.time() - t0
    # note we're returning two outputs, with the second being to a hidden div
    return "retrieved {name} in {t:.2f} seconds".format(name=name, t=time_taken),  name


@app.callback(
    output=Output(component_id='hello-output', component_property='children'),
    inputs=[Input('hello-button', 'n_clicks')],
    state=[State('hidden-output', 'children')]
)
def update_hello_div(n_clicks, name):
    if name is None:
        return "I don't know you!"
    return "hello, {name}".format(name=name)


@app.callback(
    output=Output(component_id='goodbye-output', component_property='children'),
    inputs=[Input('goodbye-button', 'n_clicks')],
    state=[State('hidden-output', 'children')]
)
def update_goodbye_div(n_clicks, name):
    if name is None:
        return "I don't know you!"
    return "goodbye, {name}".format(name=name)


if __name__ == '__main__':
    app.run_server(debug=True)
